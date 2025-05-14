import secrets
import string

def generate_reset_code(length=32):
    """Generate a secure random code for password reset"""
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))