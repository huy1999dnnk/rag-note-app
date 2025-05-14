import logging
import boto3  # Ensure boto3 is installed in the Celery worker environment
from botocore.exceptions import ClientError

from app.worker import celery_app  # Import the configured celery_app from worker.py
from app.config import settings

# Import services (these should not configure mappers themselves)
from app.services.pdf_service import PDFService
from app.services.vector_service import VectorService

# Import models for type hinting and direct use within tasks.
# Mappers are assumed to be configured by the worker's startup sequence.
from app.models.workspace import Workspace
from app.models.note import Note
from app.models.document_embedding import DocumentEmbedding, EmbeddingSource
from app.models.user import User

from app.db.database import SessionLocal  # For creating DB sessions per task

logger = logging.getLogger(__name__)


@celery_app.task(name="process_pdf")
def process_pdf_from_s3(object_key: str, note_id: str):
    """Celery task to process PDF from S3 and index in vector database"""
    logger.info(f"Starting PDF processing task for {object_key}, note_id: {note_id}")

    # Create DB session for this task
    db = SessionLocal()

    try:
        # Initialize S3 client
        s3_client = boto3.client(
            "s3",
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION,
        )

        logger.info(f"Downloading from S3: {object_key}")
        # Download file from S3
        response = s3_client.get_object(Bucket=settings.AWS_BUCKET_NAME, Key=object_key)

        # Extract file content
        file_content = response["Body"].read()
        filename = object_key.split("/")[-1]  # Extract filename from key

        logger.info(f"Downloaded {filename}, size: {len(file_content)} bytes")

        # Extract text from PDF
        pdf_service = PDFService()
        extracted_text = pdf_service.extract_text_from_pdf_bytes(file_content)

        if not extracted_text:
            logger.warning(f"No text extracted from PDF {filename}")
            return {"status": "empty", "message": "No text extracted from PDF"}

        logger.info(f"Extracted {len(extracted_text)} characters from PDF")

        # Index the PDF content
        vector_service = VectorService()
        vector_service.index_pdf_content(
            note_id=note_id,
            pdf_content=extracted_text,
            filename=filename,
            db=db,
        )

        logger.info(f"Successfully indexed PDF {filename} for note {note_id}")
        return {"status": "success", "message": "PDF processed successfully"}

    except ClientError as e:
        error_msg = f"S3 error: {str(e)}"
        logger.exception(error_msg)
        return {"status": "error", "message": error_msg}
    except Exception as e:
        error_msg = f"Error processing PDF: {str(e)}"
        logger.exception(error_msg)
        return {"status": "error", "message": error_msg}
    finally:
        db.close()
        logger.info("Database session closed")
