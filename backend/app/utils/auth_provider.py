from fastapi import HTTPException
from app.providers.google_auth_provider import GoogleAuthProvider

# Create instances once at module level
google_provider = GoogleAuthProvider()


def get_auth_provider(provider: str):
    providers = {
        "google": google_provider,
        # Add more providers here in the future
    }
    if provider not in providers:
        raise HTTPException(
            status_code=404, detail=f"Provider {provider} not supported"
        )
    return providers[provider]
