from fastapi import Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.controllers.auth_controller import AuthController
from app.schemas.auth_schemas import (
    PasswordResetRequest,
    PasswordResetVerify,
    User,
    UserCreate,
    TokenResponse,
    RefreshToken,
    UserLogin,
    AuthResponse,
)
from app.utils.jwt import get_current_user
from app.models.user import User as UserModel
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.utils.api_router import CustomApiRouter

security = HTTPBearer()

router = CustomApiRouter(tags=["authentication"])


@router.post("/register", response_model=AuthResponse)
async def register(user: UserCreate, db: Session = Depends(get_db)):
    """Register a new user"""
    return AuthController.register(user, db)


@router.post("/login", response_model=AuthResponse)
async def login(user: UserLogin, db: Session = Depends(get_db)):
    """Login to get access and refresh tokens"""
    return AuthController.login(user, db)


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(token_data: RefreshToken, db: Session = Depends(get_db)):
    """Get new tokens using refresh token"""
    return AuthController.refresh_access_token(token_data, db)


@router.post("/logout")
async def logout(
    refresh_token: RefreshToken, token: HTTPAuthorizationCredentials = Depends(security)
):
    """Logout by revoking refresh token"""
    return AuthController.logout(refresh_token, token)


@router.post("/users/me", response_model=User)
async def read_users_me(current_user: UserModel = Depends(get_current_user)):
    """Get current user information"""
    return current_user


@router.get("/protected")
async def protected_route(current_user: UserModel = Depends(get_current_user)):
    """Protected route example"""
    return {"message": f"Hello, {current_user.email}! This is a protected route."}


@router.post("/password-reset/request", response_model=dict)
async def request_password_reset(
    data: PasswordResetRequest, db: Session = Depends(get_db)
):
    """Request password reset"""
    return AuthController.request_password_reset(data, db)


@router.post("/password-reset/verify", response_model=dict)
async def verify_reset_code_and_update_password(
    data: PasswordResetVerify, db: Session = Depends(get_db)
):
    """Verify password reset code and update password"""
    return AuthController.verify_reset_code_and_update_password(data, db)
