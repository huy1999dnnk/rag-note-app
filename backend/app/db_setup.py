import logging
from sqlalchemy.orm import configure_mappers

# Import all your model classes here
# This ensures they are all defined and registered with your Base metadata
# before configure_mappers is called.
from app.models.user import User
from app.models.workspace import Workspace
from app.models.note import Note
from app.models.document_embedding import DocumentEmbedding, EmbeddingSource

# Add any other models you have

logger = logging.getLogger(__name__)


def setup_database_mappers():
    """
    Configures SQLAlchemy mappers. Call this once at application startup.
    """
    try:
        configure_mappers()
        logger.info("SQLAlchemy mappers configured successfully.")
    except Exception as e:
        logger.error(f"Error configuring SQLAlchemy mappers: {e}", exc_info=True)
        raise
