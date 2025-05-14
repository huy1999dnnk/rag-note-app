from fastapi import Depends
from app.controllers.note_controller import NoteController
from uuid import UUID
from sqlalchemy.orm import Session
from app.db.database import get_db
from typing import List, Dict, Any, Tuple
from app.utils.jwt import get_current_user
from app.schemas.note_schemas import (
    AddNewNoteBody,
    NotePreview,
    UpdateNoteBody,
    UpdateNoteTitleBody,
)
from app.utils.api_router import CustomApiRouter

router = CustomApiRouter(tags=["notes"])


@router.get(
    "/{workspace_id}",
    response_model=List[NotePreview],
    dependencies=[Depends(get_current_user)],
)
async def get_all_notes(
    workspace_id: UUID,
    db: Session = Depends(get_db),
):
    """
    Get all notes for a specific workspace.
    """
    return NoteController.get_all_notes_by_workspace_id(workspace_id, db)


@router.post(
    "/", response_model=Dict[str, Any], dependencies=[Depends(get_current_user)]
)
async def add_new_note(
    data: AddNewNoteBody,
    db: Session = Depends(get_db),
    current_user: Dict = Depends(get_current_user),
):
    """
    Create a new note.
    """
    return NoteController.create_new_note(
        data.workspace_id, data.title, db, current_user
    )


@router.put(
    "/title", response_model=Dict[str, Any], dependencies=[Depends(get_current_user)]
)
async def update_note_title(
    data: UpdateNoteTitleBody,
    db: Session = Depends(get_db),
):
    """
    Update a note's title.
    """
    return NoteController.update_note_title(data.id, data.title, db)


@router.put(
    "/content", response_model=Dict[str, Any], dependencies=[Depends(get_current_user)]
)
async def update_note_content(
    data: UpdateNoteBody,
    db: Session = Depends(get_db),
):
    """
    Update a note's content.
    """
    return NoteController.update_note_content(data.note_id, data.content, db)


@router.delete(
    "/{note_id}",
    response_model=Dict[str, Any],
    dependencies=[Depends(get_current_user)],
)
async def delete_note(
    note_id: UUID,
    db: Session = Depends(get_db),
):
    """
    Delete a note by its ID.
    """
    return NoteController.delete_note_by_id(note_id, db)


@router.get(
    "/{note_id}/content",
    response_model=Dict[str, Any],
    dependencies=[Depends(get_current_user)],
)
async def get_note_content(
    note_id: UUID,
    db: Session = Depends(get_db),
):
    """
    Get a note by its ID.
    """
    return NoteController.get_note_content_by_id(note_id, db)
