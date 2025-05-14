from fastapi import Depends
from sqlalchemy.orm import Session
from app.services.user_service import UserService
from app.schemas.user_schemas import ProfileUpdatePayload
from app.models.user import User as UserModel
from app.utils.jwt import get_current_user

class UserController:
    @staticmethod
    def get_profile(user_id: int, db: Session):
        return UserService.get_profile(user_id, db)  
    
    @staticmethod
    def update_avatar_user(user_id: int, object_key_s3: str, db: Session):
        return UserService.update_avatar_user(user_id, object_key_s3, db)
    
    @staticmethod
    def update_user_profile(data: ProfileUpdatePayload,
        db: Session, current_user: UserModel = Depends(get_current_user), ):
        return UserService.update_user_profile(data, current_user, db)
    