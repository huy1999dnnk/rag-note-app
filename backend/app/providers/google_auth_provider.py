from typing import Any, Dict
from app.interface.SocialAuthProvider import SocialAuthProvider
import httpx
from urllib.parse import urlencode
from app.config import settings

class GoogleAuthProvider():
    """Google OAuth service implementation."""
   
    def __init__(self):
        self.client_id = settings.GOOGLE_CLIENT_ID
        self.client_secret = settings.GOOGLE_CLIENT_SECRET
        self.redirect_uri = settings.GOOGLE_REDIRECT_URI
        self.scopes = settings.GOOGLE_SCOPES
        self.auth_url = 'https://accounts.google.com/o/oauth2/auth'
        self.token_url = 'https://oauth2.googleapis.com/token'
        self.user_info_url = 'https://www.googleapis.com/oauth2/v3/userinfo'

   
    async def get_user_info(self, token: str) -> dict:
        """Get user information from Google using the access token."""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                self.user_info_url,
                headers={'Authorization': f'Bearer {token}'}
            )
            response.raise_for_status()
            return response.json()

   
    def get_auth_url(self) -> str:
        """Get the authorization URL for Google OAuth."""
        params = {
            'client_id': self.client_id,
            'redirect_uri': self.redirect_uri,
            'response_type': 'code',
            'scope': self.scopes,
            'access_type': 'offline',
            "include_granted_scopes": "true",
        }
        return f"{self.auth_url}?{urlencode(params)}"

    
    async def process_callback(self, code: str) -> Dict[str, Any]:
        """Exchange authorization code for tokens and user info"""
        # Exchange code for tokens
        token_data = await self._get_token(code)
        access_token = token_data.get("access_token")
        
        # Get user info using the access token
        user_info = await self.get_user_info(access_token)
        
        # Return combined data
        return {
            "provider": "google",
            "tokens": token_data,
            "user_info": user_info
        }
      
  
    async def _get_token(self, code: str) -> Dict[str, Any]:
        """Exchange authorization code for tokens"""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.token_url,
                data={
                    "code": code,
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                    "redirect_uri": self.redirect_uri,
                    "grant_type": "authorization_code"
                }
            )
            response.raise_for_status()
            return response.json()