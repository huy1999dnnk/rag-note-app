from fastapi import Depends, Body
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.controllers.user_controller import UserController
from app.utils.jwt import get_current_user
from app.models.user import User as UserModel
from app.schemas.user_schemas import ProfileUpdatePayload, UserAvatarUpdatePayload
from app.utils.api_router import CustomApiRouter

router = CustomApiRouter(tags=["user"])


@router.put("/profile", response_model=dict, dependencies=[Depends(get_current_user)])
async def update_user_profile(
    data: ProfileUpdatePayload = Body(),
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Update the user's profile.
    """
    return UserController.update_user_profile(data, db, current_user)


@router.post("/profile", response_model=dict)
async def read_users_me(
    current_user: UserModel = Depends(get_current_user), db: Session = Depends(get_db)
):
    return UserController.get_profile(current_user.id, db)


@router.post(
    "/update-avatar-user", response_model=dict, dependencies=[Depends(get_current_user)]
)
async def update_avatar_user(
    data: UserAvatarUpdatePayload,
    db: Session = Depends(get_db),
):
    """
    Update the user's avatar.
    """
    return UserController.update_avatar_user(data.user_id, data.object_key_s3, db)
