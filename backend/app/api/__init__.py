import time
from collections.abc import Callable

from fastapi import FastAPI, Request, Response
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from pydantic_core import ValidationError as PydanticValidationError
from sqlalchemy.exc import SQLAlchemyError

from app.api import controllers as controllers_pkg
from app.api.handlers import (
    authentication_error_handler,
    bad_request_exception_handler,
    conflict_exception_handler,
    default_exception_handler,
    http_exception_handler,
    not_found_exception_handler,
    pydantic_validation_exception_handler,
    sqlalchemy_exception_handler,
    validation_exception_handler,
)
from app.config import settings
from app.core.exceptions import (
    AuthenticationError,
    BadRequestException,
    ConflictException,
    NotFoundException,
)
from app.infra.discovery import discover_submodules


def include_routes(app: FastAPI) -> None:
    """Discover and attach the `router` of every `app/api/controllers/*.py`."""

    for module in discover_submodules(controllers_pkg):
        if hasattr(module, 'router'):
            app.include_router(module.router)


def include_exception_handlers(app: FastAPI) -> None:
    """Include all exception handlers in the FastAPI app."""

    app.add_exception_handler(NotFoundException, not_found_exception_handler)
    app.add_exception_handler(BadRequestException, bad_request_exception_handler)
    app.add_exception_handler(ConflictException, conflict_exception_handler)
    app.add_exception_handler(AuthenticationError, authentication_error_handler)
    app.add_exception_handler(Exception, default_exception_handler)
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(SQLAlchemyError, sqlalchemy_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(
        PydanticValidationError, pydantic_validation_exception_handler
    )


def include_middlewares(app: FastAPI) -> None:
    """Include all middlewares in the FastAPI app."""

    @app.middleware('http')
    async def add_process_time_header(request: Request, call_next: Callable):  # type: ignore
        start_time = time.perf_counter()
        response: Response = await call_next(request)  # type: ignore
        process_time = time.perf_counter() - start_time
        response.headers['X-Process-Time'] = f'{process_time:.3f}s'  # type: ignore
        return response  # type: ignore

    if settings.env == 'development':
        app.add_middleware(
            CORSMiddleware,
            allow_origins=['http://localhost:5173'],
            allow_credentials=True,
            allow_methods=['*'],
            allow_headers=['*'],
        )
