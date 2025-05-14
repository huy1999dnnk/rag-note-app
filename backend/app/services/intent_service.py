from mistralai import Mistral, UserMessage, SystemMessage
from app.config import settings

class IntentService:
    def __init__(self):
        self.mistral = Mistral(api_key=settings.MISTRAL_API_KEY)
        self.model = "mistral-small-2503"  # Use a fast/small model for intent

    def detect_intent(self, user_message: str) -> str:
        system_prompt = (
            "You are an intent classifier for a note-taking app. "
            "Given a user message, classify the intent as one of: "
            "summarize_note, summarize_all_notes, ask_question"
            "if user ask you to do some action like: create note, delete note, update note, create workspace, delete workspace, update workspace, update profile then response with 'will_support_in_future' "
            "Return only the intent keyword."
        )
        messages = [
            SystemMessage(role="system", content=system_prompt),
            UserMessage(role="user", content=user_message),
        ]
        response = self.mistral.chat.complete(model=self.model, messages=messages)
        return response.choices[0].message.content.strip()