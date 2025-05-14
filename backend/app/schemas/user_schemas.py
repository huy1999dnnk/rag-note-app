from pydantic import BaseModel
from typing import Literal


class ProfileUpdatePayload(BaseModel):
    username: str | None
    current_password: str | None
    new_password: str | None
    type_auth: Literal["social", "local"]

    class Config:
        from_attributes = True


class UserAvatarUpdatePayload(BaseModel):
    object_key_s3: str
    user_id: int

    class Config:
        from_attributes = True
