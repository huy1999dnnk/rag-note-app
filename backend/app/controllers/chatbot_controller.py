from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from fastapi.responses import StreamingResponse
from app.db.database import get_db
from app.models.user import User
from app.utils.jwt import get_current_user
from app.schemas.chatbot_schemas import RAGChatRequest
from app.services.rag_chatbot_service import RAGChatbotService
from app.schemas.file_schemas import PdfUploadRequest
from app.models.note import Note


class ChatbotController:
    def rag_chat(
        req: RAGChatRequest,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
    ):
        chatbot = RAGChatbotService()
        return StreamingResponse(
            chatbot.answer(
                req.message, current_user.id, db, req.note_ids, req.chat_history
            ),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "X-Accel-Buffering": "no",  # For NGINX
            },
        )

    def process_pdf_for_vector_db(
        data: PdfUploadRequest,
        db: Session = Depends(get_db),
    ):
        object_key = data.objectKey
        note_id = data.noteId

        if not object_key or not note_id:
            raise HTTPException(
                status_code=400, detail="Object key and note ID are required"
            )

        # Verify the note belongs to the current user
        note = db.query(Note).filter(Note.id == note_id).first()

        if not note:
            raise HTTPException(
                status_code=404, detail="Note not found or access denied"
            )

        from app.tasks import process_pdf_from_s3

        task = process_pdf_from_s3.delay(object_key, note_id)

        return {
            "status": "success",
            "message": "PDF processing has been queued",
            "taskId": task.id,  # Return the Celery task ID
        }
