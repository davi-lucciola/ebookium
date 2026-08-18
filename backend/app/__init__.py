from collections.abc import Callable
from contextlib import AbstractAsyncContextManager, asynccontextmanager
from pathlib import Path

from fastapi import FastAPI

from app import api
from app.api.docs import swagger_metadata
from app.config import settings


@asynccontextmanager
async def default_lifespan(app: FastAPI):
    # Startup hooks (scheduler, connections, ...) go here — none yet.
    try:
        yield
    finally:
        pass  # Shutdown hooks


def create_app(
    title: str,
    description: str = '',
    version: str = '0.1.0',
    docs_url: str | None = '/api/docs',
    redoc_url: str | None = '/api/redoc',
    lifespan: Callable[[FastAPI], AbstractAsyncContextManager[None]] = default_lifespan,
) -> FastAPI:
    app = FastAPI(
        title=title,
        description=description,
        version=version,
        docs_url=docs_url,
        redoc_url=redoc_url,
        lifespan=lifespan,
        openapi_tags=swagger_metadata,
    )

    api.include_routes(app)
    api.include_middlewares(app)
    api.include_exception_handlers(app)

    if settings.env != 'development':
        frontend_dist = Path(__file__).resolve().parent.parent.parent / 'frontend' / 'dist'
        app.frontend('/', directory=str(frontend_dist), fallback='index.html')

    return app
