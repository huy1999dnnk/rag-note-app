from datetime import datetime
from pydantic import BaseModel
from uuid import UUID

class WorkspaceBody(BaseModel):
    name: str
    parent_id: UUID | None = None
    
class WorkspaceUpdateParentBody(BaseModel):
    parent_id: UUID | None = None
    id: UUID
    
class WorkspaceUpdateNameBody(BaseModel):
    name: str
    id: UUID
    
class WorkspaceSchema(BaseModel):
    id: UUID
    name: str
    parent_id: UUID | None
    user_id: int
    created_at: datetime | None
    updated_at: datetime | None

    class Config:
        from_attributes = True
    