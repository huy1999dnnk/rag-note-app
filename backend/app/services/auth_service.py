from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from jose import jwt, ExpiredSignatureError
from app.db.redis_client import redis_client
from app.models.user import User
from app.utils.password import hash_password
from app.utils.jwt import create_jwt_token
from app.config import settings
from app.schemas.auth_schemas import RefreshToken
from app.utils.utils import generate_reset_code
from app.services.email_service import EmailService
from app.services.user_service import UserService
import uuid

email_service = EmailService()


def register_user(db: Session, email: str, password: str) -> User:
    db_user = UserService.get_user_by_email(db, email)

    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    hashed_password = hash_password(password)
    db_user = User(email=email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_tokens_for_user(user: User) -> dict:
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    jti = str(uuid.uuid4())

    access_token = create_jwt_token(
        data={"sub": str(user.id), "jti": jti},
        expires_delta=access_token_expires,
    )

    refresh_token = create_jwt_token(
        data={"sub": str(user.id), "type": "refresh"},
        expires_delta=refresh_token_expires,
    )

    # Store the refresh token in Redis with an expiration time
    redis_client.set(
        f"refresh_token:{refresh_token}", user.id, ex=refresh_token_expires
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


def validate_refresh_token(refresh_token: str):
    """Validate refresh token from Redis"""
    user_id = redis_client.get(f"refresh_token:{refresh_token}")

    if user_id is None:
        return None

    return int(user_id)


def revoke_refresh_token(refresh_token: str):
    redis_client.delete(f"refresh_token:{refresh_token}")


def logout(token_data: RefreshToken, token: HTTPAuthorizationCredentials):
    """
    Logout the user by revoking the refresh token.
    """
    try:
        payload = jwt.decode(
            token.credentials,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
            options={"verify_signature": True},
        )

        jti = payload.get("jti")
        exp = payload.get("exp")
        ttl = int(exp - datetime.now(timezone.utc).timestamp())
        if jti:
            redis_client.set(f"blacklist:{jti}", "true", ex=ttl)
        revoke_refresh_token(token_data.refresh_token)
        return {"message": "Successfully logged out"}
    except ExpiredSignatureError:
        revoke_refresh_token(token_data.refresh_token)
        return {"message": "Successfully logged out"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to logout",
        )


def request_password_reset(email: str, db: Session):
    user = UserService.get_user_by_email(db, email)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Email not found",
        )

    reset_code = generate_reset_code()

    expiry = settings.PASSWORD_RESET_CODE_EXPIRE_MINUTES * 60

    redis_client.set(f"password_reset:{reset_code}", str(user.id), ex=expiry)

    resent_link = f"{settings.FRONTEND_URL_DEV}/auth/reset-password?code={reset_code}"

    email_service.send_email(
        recipient_email=email,
        subject="Password Reset Request",
        body_text=f"Click here to reset your password: {resent_link}",
        body_html=f"<p>Click here to reset your password: <a href='{resent_link}'>{resent_link}</a></p>",
    )

    return {"message": "Password reset email sent successfully"}


def verify_reset_code_and_update_password(code: str, new_password: str, db: Session):
    user_id = redis_client.get(f"password_reset:{code}")

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired reset code",
        )

    user = UserService.get_user_by_id(db, int(user_id))

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    hashed_password = hash_password(new_password)
    user.hashed_password = hashed_password
    db.commit()

    redis_client.delete(f"password_reset:{code}")

    return {"message": "Password updated successfully"}
