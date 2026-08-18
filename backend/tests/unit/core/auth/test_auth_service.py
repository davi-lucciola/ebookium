from datetime import UTC, datetime, timedelta
from unittest.mock import AsyncMock

import jwt
import pytest

from app.core.auth.services import AuthService
from app.core.exceptions import AuthenticationError
from app.core.users.models import User
from app.infra.auth import token


@pytest.fixture
def user_service() -> AsyncMock:
    return AsyncMock()


@pytest.fixture
def auth_service(user_service: AsyncMock) -> AuthService:
    return AuthService(user_service=user_service)


@pytest.fixture
def access_token(user: User) -> str:
    return token.encode_token(token.get_claims(user.id, token_type='access'))


@pytest.fixture
def refresh_jwt(user: User) -> str:
    return token.encode_token(token.get_claims(user.id, token_type='refresh'))


async def test_authenticate_returns_the_user_of_a_valid_token(
    auth_service: AuthService,
    user_service: AsyncMock,
    user: User,
    access_token: str,
) -> None:
    user_service.find_by_id.return_value = user

    result = await auth_service.authenticate(access_token)

    assert result is user
    user_service.find_by_id.assert_awaited_once_with(user.id)


async def test_authenticate_expired_token_raises_authentication_error(
    auth_service: AuthService, monkeypatch: pytest.MonkeyPatch
) -> None:
    def raise_expired(_: str) -> None:
        raise jwt.ExpiredSignatureError()

    monkeypatch.setattr(token, 'decode_token', raise_expired)

    with pytest.raises(AuthenticationError, match='Expired token.'):
        await auth_service.authenticate('any-token')


async def test_authenticate_malformed_token_raises_authentication_error(
    auth_service: AuthService,
) -> None:
    with pytest.raises(AuthenticationError, match='Invalid token.'):
        await auth_service.authenticate('not-a-jwt')


async def test_authenticate_refresh_token_raises_authentication_error(
    auth_service: AuthService, refresh_jwt: str
) -> None:
    with pytest.raises(AuthenticationError, match='Invalid token.'):
        await auth_service.authenticate(refresh_jwt)


async def test_authenticate_unknown_user_raises_authentication_error(
    auth_service: AuthService, user_service: AsyncMock, access_token: str
) -> None:
    user_service.find_by_id.return_value = None

    with pytest.raises(AuthenticationError, match='User not found.'):
        await auth_service.authenticate(access_token)


async def test_authenticate_inactive_user_raises_authentication_error(
    auth_service: AuthService,
    user_service: AsyncMock,
    user: User,
    access_token: str,
) -> None:
    user.is_active = False
    user_service.find_by_id.return_value = user

    with pytest.raises(AuthenticationError, match='User not found.'):
        await auth_service.authenticate(access_token)


async def test_login_returns_the_user_for_valid_credentials(
    auth_service: AuthService, user_service: AsyncMock, user: User
) -> None:
    user_service.find_by_email.return_value = user

    result = await auth_service.login('davi@email.com', 'secret')

    assert result is user
    user_service.find_by_email.assert_awaited_once_with('davi@email.com')


async def test_login_unknown_email_raises_authentication_error(
    auth_service: AuthService, user_service: AsyncMock
) -> None:
    user_service.find_by_email.return_value = None

    with pytest.raises(AuthenticationError, match='Invalid credentials.'):
        await auth_service.login('ghost@email.com', 'secret')


async def test_login_wrong_password_raises_authentication_error(
    auth_service: AuthService, user_service: AsyncMock, user: User
) -> None:
    user_service.find_by_email.return_value = user

    with pytest.raises(AuthenticationError, match='Invalid credentials.'):
        await auth_service.login('davi@email.com', 'wrong-password')


def test_issue_session_returns_access_and_refresh_jwts(
    auth_service: AuthService, user: User
) -> None:
    access_token, refresh_token = auth_service.issue_session(user)

    access_claims = token.decode_token(access_token)
    refresh_claims = token.decode_token(refresh_token)

    assert access_claims['sub'] == str(user.id)
    assert access_claims['typ'] == 'access'
    assert refresh_claims['sub'] == str(user.id)
    assert refresh_claims['typ'] == 'refresh'
    assert access_token != refresh_token


async def test_rotate_session_issues_a_new_cookie_pair(
    auth_service: AuthService,
    user_service: AsyncMock,
    user: User,
    refresh_jwt: str,
) -> None:
    user_service.find_by_id.return_value = user

    rotated_user, access_token, new_refresh = await auth_service.rotate_session(
        refresh_jwt
    )

    assert rotated_user is user
    assert new_refresh != refresh_jwt
    assert token.decode_token(access_token)['typ'] == 'access'
    assert token.decode_token(new_refresh)['typ'] == 'refresh'
    user_service.find_by_id.assert_awaited_once_with(user.id)


async def test_rotate_session_rejects_an_access_token(
    auth_service: AuthService, access_token: str
) -> None:
    with pytest.raises(AuthenticationError, match='Invalid token.'):
        await auth_service.rotate_session(access_token)


async def test_rotate_session_malformed_token_raises_authentication_error(
    auth_service: AuthService,
) -> None:
    with pytest.raises(AuthenticationError, match='Invalid token.'):
        await auth_service.rotate_session('not-a-jwt')


async def test_rotate_session_expired_token_raises_authentication_error(
    auth_service: AuthService, user: User
) -> None:
    claims = token.get_claims(user.id, token_type='refresh')
    claims['exp'] = datetime.now(UTC) - timedelta(seconds=1)

    with pytest.raises(AuthenticationError, match='Expired token.'):
        await auth_service.rotate_session(token.encode_token(claims))
