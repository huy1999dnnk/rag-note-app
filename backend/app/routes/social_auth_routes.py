from fastapi import Depends, Body
from sqlalchemy.orm import Session
from app.controllers.auth_controller import AuthController
from app.db.database import get_db
from app.schemas.auth_schemas import CodeSocialAuth
from app.utils.api_router import CustomApiRouter

router = CustomApiRouter()


@router.get("/{provider}/login")
async def social_login(provider: str):
    """
    Redirect to the social login page for the specified provider.
    """
    return await AuthController.social_login(provider)


@router.get("/{provider}/callback")
async def social_callback(provider: str, code: str):
    """
    Handle the callback from the social login provider.
    """
    return await AuthController.social_callback(provider, code)


@router.post("/{provider}/token")
async def social_token(
    provider: str, body: CodeSocialAuth = Body(), db: Session = Depends(get_db)
):
    """
    Handle the token exchange for the social login provider.
    """
    return await AuthController.social_token(provider, body, db)
