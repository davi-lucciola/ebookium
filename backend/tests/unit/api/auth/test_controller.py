from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi import Request, Response

from app.api.controllers.auth import (
    create_session,
    create_user,
    delete_session,
    get_me,
    refresh_session,
)
from app.api.schemas import ApiResponse
from app.core.auth.schemas import LoginIn
from app.core.exceptions import AuthenticationError
from app.core.users.models import User
from app.core.users.schemas import UserIn
from app.infra.auth.cookies import ACCESS_COOKIE_NAME, REFRESH_COOKIE_NAME


@pytest.fixture
def login_in() -> LoginIn:
    return LoginIn(email='davi@email.com', password='secret')


@pytest.fixture
def user_in() -> UserIn:
    return UserIn(name='Test User', email='davi@email.com', password='secret')


async def test_create_user_returns_an_api_response(user: User, user_in: UserIn) -> None:
    user_service = AsyncMock()
    user_service.create.return_value = user

    result = await create_user(user_in, user_service=user_service)

    assert isinstance(result, ApiResponse)
    assert result.message == 'User created successfully.'
    assert result.data is user
    user_service.create.assert_awaited_once_with(user_in)


async def test_create_session_sets_both_cookies_and_returns_the_user(
    user: User, login_in: LoginIn
) -> None:
    auth_service = AsyncMock()
    auth_service.login.return_value = user
    auth_service.issue_session = MagicMock(return_value=('access-jwt', 'refresh-jwt'))
    response = Response()

    result = await create_session(login_in, response, auth_service=auth_service)

    assert result is user
    cookies = response.headers.getlist('set-cookie')
    assert any(ACCESS_COOKIE_NAME in cookie for cookie in cookies)
    assert any(REFRESH_COOKIE_NAME in cookie for cookie in cookies)
    assert 'access-jwt' in ''.join(cookies)
    assert 'refresh-jwt' in ''.join(cookies)


async def test_refresh_session_without_cookie_raises_authentication_error() -> None:
    request = _request(cookies={})
    auth_service = AsyncMock()

    with pytest.raises(AuthenticationError, match='Authentication required.'):
        await refresh_session(request, Response(), auth_service=auth_service)

    auth_service.rotate_session.assert_not_awaited()


async def test_refresh_session_rotates_cookies(user: User) -> None:
    request = _request(cookies={REFRESH_COOKIE_NAME: 'old-refresh'})
    auth_service = AsyncMock()
    auth_service.rotate_session.return_value = (user, 'new-access', 'new-refresh')
    response = Response()

    result = await refresh_session(request, response, auth_service=auth_service)

    assert result is user
    auth_service.rotate_session.assert_awaited_once_with('old-refresh')
    cookies = ''.join(response.headers.getlist('set-cookie'))
    assert 'new-access' in cookies
    assert 'new-refresh' in cookies


async def test_delete_session_clears_cookies() -> None:
    response = Response()

    result = await delete_session(response)

    assert result is None
    cookies = ''.join(response.headers.getlist('set-cookie'))
    assert ACCESS_COOKIE_NAME in cookies
    assert REFRESH_COOKIE_NAME in cookies


async def test_get_me_returns_the_current_user(user: User) -> None:
    result = await get_me(current_user=user)

    assert result is user


def _request(cookies: dict[str, str]) -> Request:
    header_value = '; '.join(f'{name}={value}' for name, value in cookies.items())
    headers: list[tuple[bytes, bytes]] = []
    if header_value:
        headers.append((b'cookie', header_value.encode()))

    return Request({
        'type': 'http',
        'method': 'POST',
        'path': '/api/auth/session/refresh',
        'headers': headers,
        'query_string': b'',
    })
