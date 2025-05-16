import uuid
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base


def default_note_content():
    return [{"id": "1", "type": "paragraph", "props": {}, "content": []}]


class Note(Base):
    __tablename__ = "notes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    title = Column(String(255), nullable=False)
    content = Column(JSON, nullable=True, default=default_note_content)
    workspace_id = Column(
        UUID(as_uuid=True), ForeignKey("workspaces.id"), nullable=False
    )
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    embeddings = relationship(
        "DocumentEmbedding", back_populates="note", cascade="all, delete-orphan"
    )
    workspace = relationship("Workspace", back_populates="notes")
    user = relationship("User", back_populates="notes")
