from sqlalchemy import Column, DateTime, Integer, String, func
from sqlalchemy.orm import relationship
from app.db.database import Base
from app.models.social_account import SocialAccount

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=True)
    is_active = Column(Integer, default=1)
    image = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    workspaces = relationship("Workspace", back_populates="user")
    notes = relationship("Note", back_populates="user")
    social_accounts = relationship("SocialAccount", back_populates="user")
    