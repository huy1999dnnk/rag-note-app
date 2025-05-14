from sqlalchemy.orm import Session
from app.models.note import Note
from app.models.workspace import Workspace
from typing import Any, Dict, List
from fastapi import HTTPException, status
from uuid import UUID
from fastapi.encoders import jsonable_encoder
from app.schemas.note_schemas import NoteContent, NotePreview, NoteSchema
from app.services.vector_service import VectorService
from app.db.database import SessionLocal


class NoteService:
    @staticmethod
    def get_notes_by_workspace(
        db: Session, workspace_id: UUID
    ) -> List[Dict[UUID, str]]:
        """
        Get all notes for a specific workspace.
        """
        workspace = db.query(Workspace).filter(Workspace.id == workspace_id).first()
        if not workspace:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Workspace not found"
            )
        results = (
            db.query(Note.id, Note.title)
            .filter(Note.workspace_id == workspace_id)
            .order_by(Note.created_at)
            .all()
        )
        parsed_results = [NotePreview(id=id_, title=title) for id_, title in results]
        return parsed_results

    @staticmethod
    def get_note_by_id(db: Session, note_id: UUID) -> dict:
        """
        Get a note by its ID.
        """

        note = db.query(Note).filter(Note.id == note_id).first()
        if not note:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Note not found"
            )
        note_content_dict = NoteContent.model_validate(note).model_dump()
        return jsonable_encoder(note_content_dict)

    @staticmethod
    def create_note(db: Session, workspace_id: UUID, title: str, user_id: int) -> Note:
        """
        Create a new note.
        """
        new_note = Note(title=title, workspace_id=workspace_id, user_id=user_id)
        db.add(new_note)
        db.commit()
        db.refresh(new_note)
        note_dict = NoteSchema.model_validate(new_note).model_dump()
        return jsonable_encoder(note_dict)

    @staticmethod
    def update_content_note(db: Session, note_id: UUID, content: dict) -> dict:
        """
        Update the content of a note.
        """
        note = db.query(Note).filter(Note.id == note_id).first()

        if not note:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Note not found"
            )

        note.content = content
        db.commit()
        db.refresh(note)
        VectorService().debounce_index_note(
            note, db_factory=SessionLocal, wait_seconds=2
        )
        return {"content": "Note updated successfully"}

    @staticmethod
    def update_title_note(db: Session, note_id: UUID, title: str) -> dict:
        """
        Update the title of a note.
        """
        note = db.query(Note).filter(Note.id == note_id).first()

        if not note:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Note not found"
            )

        note.title = title
        db.commit()
        db.refresh(note)
        return {
            "message": "Note's title updated successfully",
        }

    @staticmethod
    def delete_note(db: Session, note_id: UUID) -> dict:
        """
        Delete a note.
        """
        note = db.query(Note).filter(Note.id == note_id).first()

        if not note:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Note not found"
            )

        db.delete(note)
        db.commit()
        return {
            "message": "Note deleted successfully",
        }
