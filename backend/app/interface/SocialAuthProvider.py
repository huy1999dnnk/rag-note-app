from typing import Dict, Any
from abc import ABC, abstractmethod

class SocialAuthProvider(ABC):
    """Base class for social authentication providers."""
    
    @abstractmethod
    def get_user_info(self, token: str) -> Dict[str, Any]:
        """Get user information from the provider using the access token."""
        pass
    
    @abstractmethod
    def get_auth_url(self, redirect_uri: str) -> str:
        """Get the authorization URL for the provider."""
        pass
    
    @abstractmethod
    async def process_callback(self, code: str) -> Dict[str, Any]:
        """Process the callback from the OAuth provider and return user info"""
        pass