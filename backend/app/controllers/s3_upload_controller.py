from app.schemas.file_schemas import GenerateUploadUrlRequest
from app.services.s3_upload_service import S3UploadService


class S3UploadController:
    @staticmethod
    def generate_presigned_upload_url(data: GenerateUploadUrlRequest):
        return S3UploadService.generate_presigned_upload_url(data)
    
    @staticmethod
    def generate_presigned_get_url(key: str, expires_in: int = 60):
        return S3UploadService.generate_presigned_get_url(key, expires_in)