from sqlalchemy import Column, Integer, DateTime, func, Text, ForeignKey, Enum, String
from app.db.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from pgvector.sqlalchemy import Vector
import uuid
import enum


# Add this Enum class
class EmbeddingSource(enum.Enum):
    NOTE_TEXT = "NOTE_TEXT"
    PDF_ATTACHMENT = "PDF_ATTACHMENT"


class DocumentEmbedding(Base):
    __tablename__ = "document_embeddings"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    note_id = Column(
        UUID(as_uuid=True), ForeignKey("notes.id", ondelete="CASCADE"), nullable=True
    )
    chunk_index = Column(Integer, nullable=False)
    content = Column(Text, nullable=False)
    embedding = Column(Vector(1536))  # Mistral embeddings are 1024-dimensional

    # Add these new columns
    source_type = Column(
        Enum(EmbeddingSource), default=EmbeddingSource.NOTE_TEXT, nullable=False
    )
    source_file = Column(String, nullable=True)  # Stores filename for PDFs

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    note = relationship("Note", back_populates="embeddings")
