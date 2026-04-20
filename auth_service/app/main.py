from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.router import router as api_router
from app.core.config import settings
from app.db.base import Base
from app.db.session import engine


@asynccontextmanager
async def lifespan(_: FastAPI):
    """Создаёт таблицы при старте приложения."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


def create_app() -> FastAPI:
    """Собирает и настраивает FastAPI приложение."""
    app = FastAPI(
        title=settings.app_name,
        lifespan=lifespan,
    )

    app.include_router(api_router)

    @app.get("/health", tags=["system"])
    async def health() -> dict[str, str]:
        return {
            "status": "ok",
            "env": settings.env,
        }

    return app


app = create_app()