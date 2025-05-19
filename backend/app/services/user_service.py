from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.services.s3_upload_service import S3UploadService
from app.models.user import User
from app.utils.password import hash_password, verify_password
from app.schemas.user_schemas import ProfileUpdatePayload


class UserService:
    @staticmethod
    def update_user_profile(
        data: ProfileUpdatePayload,
        current_user: User,
        db: Session,
    ):
        if data.username is None:
            current_user.username = ""
        else:
            username_exists = (
                db.query(User)
                .filter(
                    User.username == data.username,
                    User.id != current_user.id,
                )
                .first()
            )
            if username_exists:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Username already exists",
                )
            current_user.username = data.username

        if (
            not data.current_password
            and data.new_password
            and data.type_auth == "social"
        ):
            current_user.hashed_password = hash_password(data.new_password)
        if data.current_password or (
            data.type_auth == "local"
            and not data.current_password
            and data.new_password
        ):
            if not verify_password(data.current_password, current_user.hashed_password):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Current password is incorrect",
                )
            current_user.hashed_password = hash_password(data.new_password)

        db.commit()
        db.refresh(current_user)

        return {
            "message": "Profile updated successfully",
        }

    @staticmethod
    def update_avatar_user(
        user_id: int,
        object_key_s3: str,
        db: Session,
    ):
        user = UserService.get_user_by_id(db, user_id)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        user.image = object_key_s3
        db.commit()
        db.refresh(user)

        return {
            "message": "Avatar updated successfully",
        }

    @staticmethod
    def get_profile(user_id: int, db: Session):
        user = UserService.get_user_by_id(db, user_id)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        avatar_user_s3_key = user.image if user.image else None
        avatar_url = (
            S3UploadService.generate_presigned_get_url(avatar_user_s3_key)
            if avatar_user_s3_key
            else None
        )
        type_auth = "social" if not user.hashed_password else "local"
        return {
            "id": user.id,
            "email": user.email,
            "created_at": user.created_at,
            "updated_at": user.updated_at,
            "image": avatar_url,
            "username": user.username,
            "type_auth": type_auth,
        }

    def get_user_by_id(db: Session, user_id: int) -> User | None:
        return db.query(User).filter(User.id == user_id).first()

    def get_user_by_email(db: Session, email: str) -> User | None:
        return db.query(User).filter(User.email == email).first()

    def authenticate_user(db: Session, email: str, password: str) -> User | None:
        user = db.query(User).filter(User.email == email).first()
        if not user or not verify_password(password, user.hashed_password):
            return None
        return user
