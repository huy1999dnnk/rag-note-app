from app.config import settings
import logging
from app.exception.service_unavailable import ServiceUnavailableError
from langchain_openai import OpenAIEmbeddings
from langchain.schema import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from openai import OpenAIError
import json
import tiktoken

logger = logging.getLogger(__name__)


class OpenAiClient:

    def count_tokens_in_messages(self, messages, model="gpt-4.1-nano"):
        """
        Count tokens in a list of LangChain messages
        """
        # Get the encoding for the model
        try:
            encoding = tiktoken.encoding_for_model(model)
        except KeyError:
            # Fall back to cl100k_base for newer models not explicitly in tiktoken
            encoding = tiktoken.get_encoding("cl100k_base")

        # Per OpenAI's documentation for chat models
        tokens_per_message = (
            3  # every message follows <|start|>{role/name}\n{content}<|end|>
        )
        tokens_per_name = 1  # if there's a name, the role is omitted

        # Base tokens for the entire request
        num_tokens = 0

        # Count tokens in each message
        for message in messages:
            num_tokens += tokens_per_message

            # Count tokens in the content
            if message.content:
                num_tokens += len(encoding.encode(message.content))

            # Count tokens in the name if applicable (rare in LangChain messages)
            if hasattr(message, "name") and message.name:
                num_tokens += tokens_per_name

        # Add the final assistant reply token
        num_tokens += 3

        return num_tokens

    def serialize_langchain_messages(self, messages):
        role_map = {"system": "system", "human": "user", "ai": "assistant"}
        return [
            {"role": role_map[msg.type], "content": msg.content} for msg in messages
        ]

    def detect_if_we_need_to_search_in_vector_db(
        self, messages_for_streams, user_message
    ):
        """
        Detect if the user message requires searching in the vector database.
        """
        messages_for_streams_params = messages_for_streams[1:]
        openai_messages = self.serialize_langchain_messages(messages_for_streams_params)

        system_prompt = (
            f"You are a helpful assistant for a note-taking app. Decide if the latest user message requires vector DB search using user message and chat history: {openai_messages}\n"
            "If it can be answered from your own knowledge, return 'No'.\n"
            "Otherwise, return the keyword or phrase to search.\n"
            "Example: User: 'Do you know Adam?', Assistant: 'No', User: 'Try again' → return 'Adam'.\n"
            "Respond with only the keyword, phrase, or 'No'."
        )

        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_message),
        ]
        return self.chat(messages)

    def get_intent(self, user_message: str, messages_for_streams) -> str:
        messages_for_streams_params = messages_for_streams[1:]
        openai_messages = self.serialize_langchain_messages(messages_for_streams_params)
        system_prompt = (
            f"You are an assistant for a note-taking app. Given the user message, determine the intent based on user message and chat history:{openai_messages}.\n"
            " Return 'summarize_note' if the user wants to summarize a content of a note.\n"
            " Return 'summarize_all_notes' if the user wants to summarize all notes they have.\n"
            " Return 'delete_note+(note_id)' if the user wants to delete a note with the given ID\n"
            " Return 'general' if none of above applies (E.g: If user asking a general question or want to search info in their notes).\n"
            "Only return the intent, nothing else.\n"
        )
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_message),
        ]
        return self.chat(messages)

    def embedding_text(self, text):
        try:
            # Use the non-streaming API
            embeddings = OpenAIEmbeddings(
                openai_api_key=settings.OPENAI_API_KEY,
                model="text-embedding-3-small",
            ).embed_query(text)
            return embeddings
        except Exception as e:
            logger.error(f"Error generating embedding with LangChain: {e}")
            raise ServiceUnavailableError(
                "Sorry, the AI service is currently unavailable. Please try again later."
            )

    def chat(self, messages):
        try:
            response = ChatOpenAI(
                openai_api_key=settings.OPENAI_API_KEY,
                model="gpt-4.1-nano",
                temperature=0.2,
            ).invoke(messages)
            answer = response.content.strip()

            return answer

        except OpenAIError as e:
            logger.error(f"OpenAI API error: {e}")
            raise ServiceUnavailableError(
                "OpenAI API is currently unavailable, please try again later."
            )
        except Exception as e:
            logger.exception(f"Unexpected error calling ChatOpenAI: {e}")
            raise ServiceUnavailableError(
                "Sorry, the AI service is currently unavailable. Please try again later."
            )

    def chat_stream(self, messages):
        try:
            # Create a streaming-enabled ChatOpenAI instance
            chat = ChatOpenAI(
                openai_api_key=settings.OPENAI_API_KEY,
                streaming=True,
                model="gpt-4.1-nano",  # Or gpt-3.5-turbo for a more economical option
            )

            # Initialize an empty answer
            answer_so_far = ""

            # Use LangChain's streaming capability
            for chunk in chat.stream(messages):
                if hasattr(chunk, "content") and chunk.content:
                    # Extract the content
                    delta_content = chunk.content
                    answer_so_far += delta_content

                    # Send the incremental update as SSE
                    yield f"data: {json.dumps({'answer': answer_so_far, 'done': False})}\n\n"

            # Send the final message
            yield f"data: {json.dumps({'answer': answer_so_far, 'done': True})}\n\n"

        except OpenAIError as e:
            logger.error(f"OpenAI API error: {e}")
            error_message = "I'm currently experiencing high demand. Please try again in a few moments."
            if hasattr(e, "code") and e.code == "rate_limit_exceeded":
                error_message = "I've reached my request limit. Please try again in a few moments. 🙏"
            yield f"data: {json.dumps({'answer': error_message, 'done': True})}\n\n"
        except Exception as e:
            logger.exception(f"Unexpected error calling OpenAI API: {e}")
            yield f"data: {json.dumps({'answer': 'An unexpected error occurred. Please try again later.', 'done': True})}\n\n"
