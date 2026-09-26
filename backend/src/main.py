"""FastAPI application entrypoint."""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.config import get_settings
from src.middleware import BodySizeLimitMiddleware
from src.rag.chat.router import router as chat_router
from src.rag.chat.storage import ChatStorage
from src.rag.routes import router as rag_router
from src.rag.service import create_services

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    app.state.rag = await create_services(settings)
    # Conversation history stays readable even when the AI service is not configured.
    app.state.chat = app.state.rag.chat if app.state.rag else None
    app.state.chat_storage = (
        app.state.chat.storage if app.state.chat else ChatStorage(settings.chat_dir)
    )
    try:
        yield
    finally:
        if app.state.rag is not None:
            await app.state.rag.aclose()


app = FastAPI(title=settings.app_name, lifespan=lifespan)

app.add_middleware(
    BodySizeLimitMiddleware,
    max_bytes=settings.upload_max_request_bytes,
    path_prefixes=("/api/v1/rag/upload",),
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(rag_router, prefix="/api/v1")
app.include_router(chat_router, prefix="/api/v1")


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}
