from sqlalchemy import Column, String, ForeignKey, DateTime, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base

class SocialAccount(Base):
    __tablename__ = "social_accounts"

    id = Column(Integer,primary_key=True, index=True)
    provider = Column(String, nullable=False)
    provider_account_id = Column(String, nullable=False)
    provider_access_token = Column(String, nullable=True)
    provider_refresh_token = Column(String, nullable=True)
    provider_expires_at = Column(DateTime(timezone=True), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="social_accounts")