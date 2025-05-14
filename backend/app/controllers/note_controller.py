from typing import Dict
from sqlalchemy.orm import Session
from fastapi import Depends
from uuid import UUID
from app.db.database import get_db
from app.services.note_service import NoteService
from app.utils.jwt import get_current_user

class NoteController:
    @staticmethod
    def get_all_notes_by_workspace_id(workspace_id: UUID,db: Session = Depends(get_db)):
        """
        Get all notes for a specific workspace.
        """
        return NoteService.get_notes_by_workspace(db, workspace_id)
    
    @staticmethod
    def create_new_note(workspace_id: UUID, title: str, db: Session = Depends(get_db), current_user: Dict = Depends(get_current_user)):
        """
        Create a new note.
        """
        return NoteService.create_note(db, workspace_id, title, current_user.id)
    
    @staticmethod
    def get_note_content_by_id(note_id: UUID, db: Session = Depends(get_db)):
        """
        Get a note by its ID.
        """
        return NoteService.get_note_by_id(db, note_id)
    
    @staticmethod
    def update_note_content(note_id: UUID, content: dict, db: Session = Depends(get_db)):
        """
        Update the content of a note.
        """
        return NoteService.update_content_note(db, note_id, content)
    
    @staticmethod
    def update_note_title(note_id: UUID, title: str, db: Session = Depends(get_db)):
        """
        Update the title of a note.
        """
        return NoteService.update_title_note(db, note_id, title)
    
    @staticmethod
    def delete_note_by_id(note_id: UUID, db: Session = Depends(get_db)):
        """
        Delete a note by its ID.
        """
        return NoteService.delete_note(db, note_id)
    
    
    
    