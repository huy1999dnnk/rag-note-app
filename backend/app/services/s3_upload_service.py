from fastapi import HTTPException
from app.schemas.file_schemas import GenerateUploadUrlRequest, GenerateUploadUrlResponse
from app.config import settings
import boto3
import uuid
MAX_FILE_SIZE_MB = 10
ALLOWED_MIME_TYPES = [
  'image/jpeg',
  'image/png',
  'image/gif',
  'image/webp',
  'image/svg+xml',
  'video/mp4',
  'video/quicktime',
  'video/x-msvideo',
  'video/x-matroska',
  'video/webm',
  'application/pdf',
  'application/msword',
  'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
  'application/vnd.ms-excel',
  'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
  'application/vnd.ms-powerpoint',
  'application/vnd.openxmlformats-officedocument.presentationml.presentation',
];




s3_client = boto3.client(
    "s3",
    region_name=settings.AWS_REGION,
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
)

class S3UploadService:
    @staticmethod
    def generate_presigned_upload_url(data: GenerateUploadUrlRequest) -> GenerateUploadUrlResponse:
        if data.fileSize > MAX_FILE_SIZE_MB * 1024 * 1024:
            raise HTTPException(status_code=400, detail="File too large. Max 10MB.")

        if data.contentType not in ALLOWED_MIME_TYPES:
            raise HTTPException(status_code=400, detail="Unsupported file type.")

        file_ext = data.filename.split(".")[-1]
        file_key = f"{uuid.uuid4()}.{file_ext}"

        upload_url = s3_client.generate_presigned_url(
            "put_object",
            Params={
                "Bucket": settings.AWS_BUCKET_NAME,
                "Key": file_key,
                "ContentType": data.contentType,
            },
            ExpiresIn=900,
        )

        return GenerateUploadUrlResponse(
            uploadUrl=upload_url,
            objectKey=file_key
        )


    @staticmethod
    def generate_presigned_get_url(key: str, expires_in: int = 900) -> str:
        return s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": settings.AWS_BUCKET_NAME, "Key": key},
            ExpiresIn=expires_in,
        )
