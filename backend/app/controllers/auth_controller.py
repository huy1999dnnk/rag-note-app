from fastapi import Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from jose import JWTError, jwt, ExpiredSignatureError
from app.config import settings
from app.db.database import get_db
from app.schemas.auth_schemas import (
    CodeSocialAuth,
    PasswordResetRequest,
    PasswordResetVerify,
    UserCreate,
    RefreshToken,
    TokenResponse,
)
from app.services.auth_service import (
    register_user,
    create_tokens_for_user,
    validate_refresh_token,
    revoke_refresh_token,
    logout,
    request_password_reset,
    verify_reset_code_and_update_password,
)
from fastapi.security import HTTPAuthorizationCredentials
from app.utils.auth_provider import get_auth_provider
from app.services.google_auth_service import GoogleAuthService
from app.services.user_service import UserService


class AuthController:
    @staticmethod
    def register(
        user: UserCreate,
        db: Session = Depends(get_db),
    ) -> TokenResponse:
        db_user = register_user(db, user.email, user.password)
        tokens = create_tokens_for_user(db_user)
        return tokens

    @staticmethod
    def login(
        user: UserCreate,
        db: Session = Depends(get_db),
    ) -> TokenResponse:
        db_user = UserService.authenticate_user(db, user.email, user.password)
        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        tokens = create_tokens_for_user(db_user)
        return tokens

    @staticmethod
    def refresh_access_token(tokenData: RefreshToken, db: Session = Depends(get_db)):
        """
        Refresh the access token using the refresh token.
        """
        try:
            payload = jwt.decode(
                tokenData.refresh_token,
                settings.JWT_SECRET_KEY,
                algorithms=[settings.JWT_ALGORITHM],
                options={"verify_signature": True},
            )

            if payload.get("type") != "refresh":
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid token",
                )

            user_id = payload.get("sub")
            if not user_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid token",
                )

            # Validate the refresh token exists in Redis
            valid_user_id = validate_refresh_token(tokenData.refresh_token)
            if valid_user_id is None or valid_user_id != int(user_id):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Refresh token expired or invalid",
                )

            # Create new access token
            user = UserService.get_user_by_id(db, int(user_id))
            if not user or user.id != int(user_id):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="User not found",
                )

            revoke_refresh_token(tokenData.refresh_token)

            return create_tokens_for_user(user)
        except ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token expired",
            )
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
            )

    @staticmethod
    def logout(token_data: RefreshToken, token: HTTPAuthorizationCredentials):
        """
        Logout the user by revoking the refresh token.
        """
        try:
            logout(token_data, token)
            return {"message": "Successfully logged out"}
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to logout",
            )

    @staticmethod
    async def social_login(provider: str):
        """Redirect to the provider's authentication page"""
        auth_provider = get_auth_provider(provider)
        redirect_url = auth_provider.get_auth_url()
        return RedirectResponse(url=redirect_url)

    @staticmethod
    async def social_callback(provider: str, code: str):

        frontend_url = (
            f"{settings.FRONTEND_URL_DEV}/auth/callback/{provider}?code={code}"
        )
        return RedirectResponse(url=frontend_url)

    @staticmethod
    async def social_token(
        provider: str, params: CodeSocialAuth, db: Session = Depends(get_db)
    ):
        """Handle the callback from the OAuth provider"""
        auth_provider = get_auth_provider(provider)

        # Process callback to get tokens and user info
        try:
            auth_data = await auth_provider.process_callback(params.code)
        except Exception as e:
            raise HTTPException(
                status_code=400, detail=f"Failed to authenticate: {str(e)}"
            )

        user_info = auth_data["user_info"]

        # Validate that we have required user info
        if "sub" not in user_info or "email" not in user_info:
            raise HTTPException(
                status_code=400, detail="Missing required user information"
            )

        # Create or get user
        user = GoogleAuthService.create_or_get_user_by_social_login(
            db=db,
            provider=provider,
            provider_account_id=user_info["sub"],
            email=user_info["email"],
        )

        token_data = create_tokens_for_user(user)
        return token_data

    @staticmethod
    def request_password_reset(
        data: PasswordResetRequest, db: Session = Depends(get_db)
    ):
        return request_password_reset(data.email, db)

    @staticmethod
    def verify_reset_code_and_update_password(
        data: PasswordResetVerify, db: Session = Depends(get_db)
    ):
        return verify_reset_code_and_update_password(data.code, data.password, db)
