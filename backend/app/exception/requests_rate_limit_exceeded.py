# Add this near your imports
class RequestRateLimitExceededError(Exception):
    """Error indicating Mistral service is rate limited"""

    pass
