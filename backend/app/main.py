from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel

from app.config import settings
from app.core.errors import (
    ConflictError,
    NotFoundError,
    conflict_handler,
    not_found_handler,
)
from app.core.middleware import RequestLoggingMiddleware
from app.dependencies import engine
from app.routers import users


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator[None, None]:
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    yield


def create_app() -> FastAPI:
    application = FastAPI(
        title="My App API",
        version="0.1.0",
        lifespan=lifespan,
    )

    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    application.add_middleware(RequestLoggingMiddleware)

    application.add_exception_handler(NotFoundError, not_found_handler)  # type: ignore[arg-type]
    application.add_exception_handler(ConflictError, conflict_handler)  # type: ignore[arg-type]

    application.include_router(users.router)

    return application


app = create_app()
