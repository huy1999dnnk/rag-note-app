from fastapi import Query
from app.controllers.s3_upload_controller import S3UploadController
from app.schemas.file_schemas import GenerateUploadUrlRequest, GenerateUploadUrlResponse
from app.utils.api_router import CustomApiRouter

router = CustomApiRouter(tags=["Upload File"])


@router.post("/generate-upload-url", response_model=GenerateUploadUrlResponse)
def generate_upload_url(data: GenerateUploadUrlRequest):
    return S3UploadController.generate_presigned_upload_url(data)


@router.get("/get-image-url")
def get_image_url(key: str, expires_in: int = Query(60)):
    return {"url": S3UploadController.generate_presigned_get_url(key, expires_in)}
