from typing import List, Optional
from pydantic import BaseModel


class RAGChatRequest(BaseModel):
    message: str
    note_ids: Optional[List[str]] = None
    chat_history: Optional[List[dict]] = None
