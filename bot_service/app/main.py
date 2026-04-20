from fastapi import FastAPI

from app.core.config import settings


def create_app() -> FastAPI:
    """Создаёт FastAPI-приложение Bot Service."""
    app = FastAPI(title=settings.app_name)

    @app.get("/health", tags=["system"])
    async def health() -> dict[str, str]:
        return {
            "status": "ok",
            "env": settings.env,
        }

    return app


app = create_app()