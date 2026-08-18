import logging
from typing import cast

from fastapi import Request, status
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.responses import JSONResponse
from pydantic_core import ValidationError as PydanticValidationError

from app.api.schemas import DetailResponse, MessageResponse
from app.core.exceptions import (
    BadRequestException,
    ConflictException,
    NotFoundException,
)

logger = logging.getLogger(__name__)

error_response = MessageResponse(
    message='An unexpected problem occurred while processing your request. '
    + 'Please try again later.'
)


def default_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.error(f'{request.method} {request.url} - {exc}')

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=error_response.model_dump(),
    )


def http_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    http_exc = cast(HTTPException, exc)
    response = MessageResponse(message=http_exc.detail)

    return JSONResponse(
        status_code=http_exc.status_code,
        content=response.model_dump(),
    )


def validation_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle request body/query validation failures."""

    validation_exc = cast(RequestValidationError, exc)

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        content=DetailResponse(detail=validation_exc.errors()).model_dump(mode='json'),
    )


def pydantic_validation_exception_handler(
    request: Request, exc: Exception
) -> JSONResponse:
    """Handle Pydantic models built in code, outside the request body.

    FastAPI only turns request-body failures into `RequestValidationError`; a
    model built in code raises `pydantic_core.ValidationError`, which without
    this handler would fall through to `default_exception_handler` and become
    500.
    """

    validation_exc = cast(PydanticValidationError, exc)

    logger.error(f'{request.method} {request.url}\n{validation_exc}')

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=error_response.model_dump(),
    )


def sqlalchemy_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.error(f'{request.method} {request.url}\n{exc}')

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=error_response.model_dump(),
    )


def not_found_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    domain_exc = cast(NotFoundException, exc)
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content=MessageResponse(message=domain_exc.message).model_dump(),
    )


def bad_request_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    domain_exc = cast(BadRequestException, exc)
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=MessageResponse(message=domain_exc.message).model_dump(),
    )


def conflict_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    domain_exc = cast(ConflictException, exc)
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content=MessageResponse(message=domain_exc.message).model_dump(),
    )


def authentication_error_handler(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content=MessageResponse(message=str(exc)).model_dump(),
    )
