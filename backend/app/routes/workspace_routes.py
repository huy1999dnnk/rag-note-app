from fastapi import Depends
from app.controllers.workspace_controller import WorkspaceController
from uuid import UUID
from sqlalchemy.orm import Session
from app.db.database import get_db
from typing import List, Dict, Any
from app.utils.jwt import get_current_user
from app.schemas.workspace_schemas import (
    WorkspaceBody,
    WorkspaceUpdateNameBody,
    WorkspaceUpdateParentBody,
)
from app.utils.api_router import CustomApiRouter

router = CustomApiRouter(tags=["workspaces"])


@router.get("/", response_model=List[Dict[str, Any]])
async def get_all_workspace(
    db: Session = Depends(get_db), current_user: Dict = Depends(get_current_user)
):
    """
    Get all workspaces for the current user.
    """
    return WorkspaceController.get_all_workspace_by_user_id(db, current_user)


@router.post("/", response_model=Dict[str, Any])
async def add_new_workspace(
    data: WorkspaceBody,
    db: Session = Depends(get_db),
    current_user: Dict = Depends(get_current_user),
):
    """
    Add a new workspace for the current user.
    """
    return WorkspaceController.add_new_workspace(data, db, current_user)


@router.put(
    "/parent", response_model=Dict[str, Any], dependencies=[Depends(get_current_user)]
)
async def update_parent_workspace(
    data: WorkspaceUpdateParentBody, db: Session = Depends(get_db)
):
    """
    Update the parent of a workspace.
    """
    return WorkspaceController.update_parent_workspace(data, db)


@router.put("/name", response_model=Dict[str, Any])
async def update_workspace_name(
    data: WorkspaceUpdateNameBody, db: Session = Depends(get_db)
):
    """
    Update the name of a workspace.
    """
    return WorkspaceController.update_workspace_name(data, db)


@router.delete("/{id}", response_model=Dict[str, Any])
async def delete_workspace_and_subworkspaces(id: UUID, db: Session = Depends(get_db)):
    """
    Delete a workspace and all its sub-workspaces.
    """
    return WorkspaceController.delete_workspace_and_subworkspaces(id, db)
