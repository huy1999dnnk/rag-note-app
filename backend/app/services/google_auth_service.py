from typing import Optional
import uuid
from sqlalchemy.orm import Session
from app.models.user import User
from app.models.social_account import SocialAccount

class GoogleAuthService:
    @staticmethod
    def get_social_account(db: Session, provider: str, provider_account_id: str) -> Optional[SocialAccount]:
        """Get social account by provider and provider account ID"""
        return db.query(SocialAccount).filter(
            SocialAccount.provider == provider,
            SocialAccount.provider_account_id == provider_account_id
        ).first()

    @staticmethod
    def create_or_get_user_by_social_login(
        db: Session, 
        provider: str, 
        provider_account_id: str,
        email: str,
    ) -> User:
        """Create a new user or return existing user based on social login info"""
        # Check if we already have this social account
        social_account = GoogleAuthService.get_social_account(db, provider, provider_account_id)
        if social_account:
            # We found an existing social account, return the associated user
            return social_account.user
        
        # Check if user with this email exists
        user = db.query(User).filter(User.email == email).first()
        
        # Create new user if needed
        if not user:
            
            # Create new user with NULL password and optional profile image
            user = User(
                email=email,
                username=None,
                hashed_password=None,  # No password for social login users
                is_active=1
            )
            db.add(user)
            db.flush()
        
        # Create social account linked to this user
        social_account = SocialAccount(
            provider=provider,
            provider_account_id=provider_account_id,
            user_id=user.id,
        )
        db.add(social_account)
        db.commit()
        db.refresh(user)
        
        return user