from fastapi import Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.utils.jwt import get_current_user
from app.models.user import User as UserModel
from app.schemas.chatbot_schemas import RAGChatRequest
from app.controllers.chatbot_controller import ChatbotController
from app.schemas.file_schemas import PdfUploadRequest
from app.utils.api_router import CustomApiRouter

router = CustomApiRouter()


@router.post("/chat", response_model=dict)
def chatbot_endpoint(
    data: RAGChatRequest,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    """
    Endpoint for the chatbot.
    """
    return ChatbotController.rag_chat(data, db, current_user)


@router.post("/upload/process-pdf", dependencies=[Depends(get_current_user)])
def process_pdf_endpoint(data: PdfUploadRequest, db: Session = Depends(get_db)):
    """
    Endpoint to process PDF for vector DB.
    """
    return ChatbotController.process_pdf_for_vector_db(data, db)
