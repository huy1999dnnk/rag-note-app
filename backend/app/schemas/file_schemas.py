from pydantic import BaseModel


class GenerateUploadUrlRequest(BaseModel):
    filename: str
    contentType: str
    fileSize: int


class GenerateUploadUrlResponse(BaseModel):
    uploadUrl: str
    objectKey: str


class PdfUploadRequest(BaseModel):
    objectKey: str
    noteId: str
