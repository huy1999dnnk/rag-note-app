from app.services.vector_service import VectorService
from app.models.note import Note
from app.exception.service_unavailable import ServiceUnavailableError
from app.exception.requests_rate_limit_exceeded import RequestRateLimitExceededError
from app.services.openai_client import OpenAiClient
from langchain.schema import HumanMessage, SystemMessage, AIMessage
from sqlalchemy.orm import Session
from typing import List, Optional
from app.config import settings
from openai import OpenAIError
import logging
import json

logger = logging.getLogger(__name__)


class RAGChatbotService:
    def __init__(self):
        self.openAiClient = OpenAiClient()

    def get_text_content_from_note(self, notes: List[Note], vs: VectorService):
        """
        Extract text content from notes.
        """
        contents = [vs.extract_plain_text_from_json(note.content) for note in notes]
        return "\n\n".join(contents)

    def answer(
        self,
        user_message: str,
        user_id: str,
        db: Session,
        note_ids: List[str],
        chat_history: Optional[List[dict]] = None,
        top_k: int = 2,
    ):
        try:
            # Estimate user message tokens

            messages_for_streams = []
            messages_for_streams.append(
                SystemMessage(
                    content=(
                        "You are a helpful assistant for a note-taking app. Answer questions based on the provided context\n"
                        "If the answer isn’t in the context, use your own knowledge, but keep replies short and relevant.\n"
                        "After answering, suggest follow-up questions and ask if the user wants to know more."
                    )
                ),
            )
            if chat_history:
                for item in chat_history:
                    if item["role"] == "user":
                        messages_for_streams.append(
                            HumanMessage(content=item["content"])
                        )
                    elif item["role"] == "assistant":
                        messages_for_streams.append(AIMessage(content=item["content"]))

            vs = VectorService()
            question = self.openAiClient.detect_if_we_need_to_search_in_vector_db(
                messages_for_streams, user_message
            )

            question = json.loads(question)
            if question["type"] == "general":
                prompt = user_message
            elif question["type"] == "search":
                chunks = vs.search_similar_chunks(question["query"], db, top_k)
                context = "\n\n".join(chunks)
                prompt = f"data you might need from database:\n{context}\n\n Use the history chat and data to answer this question: {user_message}"
            elif question["type"] == "summarize_note":
                note_id = question["query"]
                notes = db.query(Note).filter(Note.id == note_id).all()

                if not notes:
                    prompt = f"Note with id {note_id} not found. Anwser the question: {user_message}"
                else:
                    context = self.get_text_content_from_note(notes, vs)
                    if not context:
                        prompt = f"Note with id {note_id} content is not summarize. Anwser the question: {user_message}"
                    else:
                        prompt = f"Summarize the following note:\n{context}\n\nUse the history chat and data to answer this question: {user_message}"
            elif question["type"] == "support_later":
                prompt = f"The action user require will be support in the future. Answer this question: {user_message}"

            messages_for_streams.append(HumanMessage(content=prompt))

            if self.openAiClient.count_tokens_in_messages(messages_for_streams) > 500:
                yield f"data: {json.dumps({'answer': 'The message is too long, please shorten it.', 'done': True, 'error_type': 'HISTORY_TOO_LONG'})}\n\n"
                return

            stream = self.openAiClient.chat_stream(messages=messages_for_streams)

            yield from stream
        except OpenAIError as openai_error:
            # Catch any generic OpenAI error
            logger.error(f"OpenAI API error: {openai_error}")
            yield f"data: {json.dumps({'answer': 'OpenAI API is currently unavailable, please try again later.', 'done': True})}\n\n"
        except RequestRateLimitExceededError as rate_limit_error:
            error_message = str(rate_limit_error)
            yield f"data: {json.dumps({'answer': f"{error_message}🙏", 'done': True})}\n\n"
        except ServiceUnavailableError as service_unavailable_error:
            error_message = str(service_unavailable_error)
            yield f"data: {json.dumps({'answer': f"{error_message}", 'done': True})}\n\n"
        except Exception as e:
            logger.exception(f"Error in RAGChatbot: {e}")
            yield f"data: {json.dumps({'answer': 'Sorry, something went wrong with the chatbot service. {e}', 'done': True})}\n\n"
