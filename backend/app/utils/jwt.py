from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError, ExpiredSignatureError
from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from app.db.redis_client import redis_client
from app.config import settings
from app.db.database import get_db
from app.models.user import User
from app.schemas.auth_schemas import TokenData

security = HTTPBearer()

def create_jwt_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    now = datetime.now(timezone.utc)
    if expires_delta:
        expire = now + expires_delta
    else:
        expire = now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt

def get_current_user(token: str = Depends(security), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token_revoke_exception = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Token has been revoked",
    )
    expired_token_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token has expired",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token.credentials, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        jti = payload.get("jti")
        if redis_client.get(f"blacklist:{jti}") == "true":
            raise token_revoke_exception
        user_id: int = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        token_data = TokenData(user_id=user_id)
    except ExpiredSignatureError:
        raise expired_token_exception
    except JWTError:
        raise credentials_exception
    user = db.query(User).filter(User.id == token_data.user_id).first()
    if user is None:
        raise credentials_exception
    return user