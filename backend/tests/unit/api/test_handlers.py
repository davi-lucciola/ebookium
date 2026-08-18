import json
from collections.abc import Callable
from typing import Any

import pytest
from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel
from pydantic_core import ValidationError as PydanticValidationError

from app.api.handlers import (
    pydantic_validation_exception_handler,
    validation_exception_handler,
)


class DemoIn(BaseModel):
    name: str
    age: int = 0


@pytest.fixture
def request_mock() -> Request:
    return Request({
        'type': 'http',
        'method': 'POST',
        'path': '/api/auth/user',
        'headers': [],
        'query_string': b'',
    })


def _body(response: Any) -> dict[str, Any]:
    return json.loads(response.body)


def _errors_from(build: Callable[[], Any]) -> list[Any]:
    """Run an invalid model constructor and return the Pydantic errors."""

    with pytest.raises(PydanticValidationError) as exc_info:
        build()

    return exc_info.value.errors()


def _build_schema_violation() -> DemoIn:
    return DemoIn()  # type: ignore[call-arg]


def test_request_validation_schema_error_returns_422(request_mock: Request) -> None:
    exc = RequestValidationError(_errors_from(_build_schema_violation))

    response = validation_exception_handler(request_mock, exc)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

    body = _body(response)
    assert body.get('message') is None
    assert body['detail'][0]['type'] == 'missing'


def test_pydantic_validation_schema_error_returns_500(request_mock: Request) -> None:
    with pytest.raises(PydanticValidationError) as exc_info:
        _build_schema_violation()

    response = pydantic_validation_exception_handler(request_mock, exc_info.value)

    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert 'unexpected' in _body(response)['message']
