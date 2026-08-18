from unittest.mock import AsyncMock

import pytest
from fastapi import HTTPException, Request, status

from app.api.guards import AuthGuard
from app.core.users.models import User


@pytest.fixture
def request_without_cookie() -> Request:
    return Request({
        'type': 'http',
        'method': 'GET',
        'path': '/api/auth/user/me',
        'headers': [],
        'query_string': b'',
    })


@pytest.fixture
def request_with_cookie() -> Request:
    return Request({
        'type': 'http',
        'method': 'GET',
        'path': '/api/auth/user/me',
        'headers': [(b'cookie', b'access_token=access-jwt')],
        'query_string': b'',
    })


async def test_auth_guard_missing_access_cookie_raises_401(
    request_without_cookie: Request,
) -> None:
    guard = AuthGuard()

    with pytest.raises(HTTPException) as exc_info:
        await guard(request_without_cookie, auth_service=AsyncMock(), _cookie=None)

    assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert exc_info.value.detail == 'Authentication required.'


async def test_auth_guard_authenticates_the_access_cookie(
    request_with_cookie: Request, user: User
) -> None:
    auth_service = AsyncMock()
    auth_service.authenticate.return_value = user
    guard = AuthGuard()

    result = await guard(
        request_with_cookie, auth_service=auth_service, _cookie='access-jwt'
    )

    assert result is user
    auth_service.authenticate.assert_awaited_once_with('access-jwt')
