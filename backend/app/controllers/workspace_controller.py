from sqlalchemy.orm import Session
from app.db.database import get_db
from fastapi import Depends
from typing import List, Dict, Any
from app.schemas.workspace_schemas import WorkspaceBody, WorkspaceUpdateNameBody, WorkspaceUpdateParentBody
from app.services.workspace_service import WorkspaceService
from app.utils.jwt import get_current_user
from uuid import UUID

class WorkspaceController:
    @staticmethod
    def get_all_workspace_by_user_id(db: Session = Depends(get_db), current_user: Dict = Depends(get_current_user)):
        return WorkspaceService.get_workspace_tree(db, current_user.id)

    @staticmethod
    def add_new_workspace(data: WorkspaceBody, db: Session = Depends(get_db), current_user: Dict = Depends(get_current_user)):
        return WorkspaceService.add_new_workspace(data,db, current_user.id)
    
    @staticmethod
    def update_parent_workspace(data: WorkspaceUpdateParentBody,db: Session = Depends(get_db)):
        return WorkspaceService.update_parent_workspace(db, data.id, data.parent_id)
    
    @staticmethod
    def update_workspace_name(data: WorkspaceUpdateNameBody,db: Session = Depends(get_db)):
        return WorkspaceService.update_workspace_name(db, data.id, data.name)
    
    @staticmethod
    def delete_workspace_and_subworkspaces(id: UUID,db: Session = Depends(get_db)):
        return WorkspaceService.delete_workspace_and_subworkspaces(db, id)