import logging

# --- STEP 1: Configure Logging (Optional but Recommended) ---
# Basic logging setup, adjust as needed.
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)
logger.info("Celery worker process starting...")

# --- STEP 2: Perform Database Mapper Setup (CRITICAL) ---
# This MUST happen before Celery app initialization and task discovery.
try:
    logger.info("Attempting to set up database mappers for Celery worker...")
    from app.db_setup import setup_database_mappers

    setup_database_mappers()  # This will import all models and configure mappers.
    logger.info("Database mappers setup COMPLETE for Celery worker.")
except Exception as e:
    logger.error(
        f"FATAL: Failed to set up database mappers for Celery worker during startup: {e}",
        exc_info=True,
    )
    # If mappers fail to set up, the worker will not function.
    # Consider exiting or raising the error to stop the worker.
    raise SystemExit(f"Mapper setup failed: {e}")

# --- STEP 3: Import Celery and Configure Celery App ---
from celery import Celery
from app.config import settings

# Initialize Celery with your project name
celery_app = Celery("task_management")

# Configure Celery using the URL from environment variables
celery_app.conf.broker_url = settings.REDIS_URL
celery_app.conf.result_backend = settings.REDIS_URL

# Additional configuration
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)

# This will automatically discover and register tasks in the specified modules
celery_app.autodiscover_tasks(["app.tasks"])
