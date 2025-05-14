from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import (
    auth_routes,
    workspace_routes,
    note_routes,
    upload_file_routes,
    social_auth_routes,
    user_routes,
    chatbot_routes,
)
from app.db.database import Base, engine
from app.config import settings

Base.metadata.create_all(bind=engine)

app = FastAPI(title="FastAPI Note Management", version="1.0.0")

origins = settings.ALLOWED_ORIGINS.split(",") if settings.ALLOWED_ORIGINS else ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_routes.router, prefix="/api/v1/auth")
app.include_router(workspace_routes.router, prefix="/api/v1/workspaces")
app.include_router(note_routes.router, prefix="/api/v1/notes")
app.include_router(upload_file_routes.router, prefix="/api/v1/upload")
app.include_router(social_auth_routes.router, prefix="/api/auth")
app.include_router(user_routes.router, prefix="/api/v1/user")
app.include_router(chatbot_routes.router, prefix="/api/v1/chatbot")


@app.get("/")
def read_root():
    return {"message": "Hello, huypm123!"}
