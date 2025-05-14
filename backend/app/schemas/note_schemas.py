from pydantic import BaseModel
from uuid import UUID
from typing import List
class NotePreview(BaseModel):
    id: UUID
    title: str
    
    class Config:
        from_attributes = True
    
class NoteSchema(BaseModel):
    id: UUID
    title: str
    content: List[dict]
    
    class Config:
        from_attributes = True
        
class AddNewNoteBody(BaseModel):
    title: str
    workspace_id: UUID
    
class UpdateNoteBody(BaseModel):
    note_id: UUID
    content: List[dict]
    
class UpdateNoteTitleBody(BaseModel):
    id: UUID
    title: str
    
class NoteContent(BaseModel):
    content: List[dict]
    
    class Config:
        from_attributes = True