from pydantic import BaseModel

class TokenData(BaseModel):
    user_id: int | None = None

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenResponse(Token):
    refresh_token: str

class RefreshToken(BaseModel):
    refresh_token: str

class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str
    
# New login schema for direct body authentication
class UserLogin(UserBase):
    password: str

class User(UserBase):
    id: int
    
    class Config:
        from_attributes = True
        
class AuthResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class CodeSocialAuth(BaseModel):
    code: str

class PasswordResetRequest(BaseModel):
    email: str

class PasswordResetVerify(BaseModel):
    code: str
    password: str