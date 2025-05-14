from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.models.workspace import Workspace
from typing import List, Dict, Any
from fastapi import HTTPException, status
from uuid import UUID
from fastapi.encoders import jsonable_encoder

from app.schemas.workspace_schemas import WorkspaceBody, WorkspaceSchema

class WorkspaceService:
    @staticmethod
    def build_workspace_tree(workspaces: List[Workspace], parent_id: UUID = None) -> List[Dict[str, Any]]:
        """
        Build a tree structure from a flat list of workspaces.
        """
        tree = []
        for workspace in workspaces:
            if workspace.parent_id == parent_id:
                children = WorkspaceService.build_workspace_tree(workspaces, workspace.id)
                node = {
                    "id": workspace.id,
                    "name": workspace.name,
                    "children": children
                }


                tree.append(node)
        return tree
    
    @staticmethod
    def get_workspace_tree(db: Session, user_id: int) -> List[Dict[str, Any]]:
        """
        Get the workspace tree for a user.
        """
        workspaces = db.query(Workspace).filter(Workspace.user_id == user_id).order_by(Workspace.created_at).all()
        return WorkspaceService.build_workspace_tree(workspaces)
    
    @staticmethod
    def add_new_workspace(data: WorkspaceBody,db: Session, user_id: int) -> Workspace:
        """
        Add a new workspace.
        """
        new_workspace = Workspace(name=data.name, user_id=user_id, parent_id=data.parent_id)
        db.add(new_workspace)
        db.commit()
        db.refresh(new_workspace)
        workspace_dict = WorkspaceSchema.model_validate(new_workspace).model_dump()
        return jsonable_encoder(workspace_dict)
    
    @staticmethod
    def update_parent_workspace(db: Session, workspace_id: UUID, parent_id: UUID | None) -> Workspace:
        """
        Update the parent of a workspace.
        """
        workspace = db.query(Workspace).filter(Workspace.id == workspace_id).first()
        
        if not workspace:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Workspace not found")
        
        
        workspace.parent_id = parent_id
        db.commit()
        db.refresh(workspace)
        workspace_dict = WorkspaceSchema.model_validate(workspace).model_dump()
        return jsonable_encoder(workspace_dict)
        
    
    @staticmethod
    def update_workspace_name(db: Session, workspace_id: UUID, name: str) -> Workspace:
        """
        Update the name of a workspace.
        """
        workspace = db.query(Workspace).filter(Workspace.id == workspace_id).first()
        if not workspace:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Workspace not found")
        
        
        workspace.name = name
        db.commit()
        db.refresh(workspace)
        workspace_dict = WorkspaceSchema.model_validate(workspace).model_dump()
        return jsonable_encoder(workspace_dict)
        
    
    @staticmethod
    def delete_workspace_and_subworkspaces(db: Session, workspace_id: UUID) -> None:
        """
        Delete a workspace and all its sub-workspaces.
        """
        workspace = db.query(Workspace).filter(Workspace.id == workspace_id).first()

        if not workspace:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Workspace not found")

        # Recursive delete helper
        def delete_children(w: Workspace):
            for child in w.children:
                delete_children(child)
            db.delete(w)

        delete_children(workspace)
        db.commit()

        return {"message": "Deleted successfully"}
        