from fastapi import Request, Response

from app.config import settings
from app.infra.auth import cookies
from app.infra.auth.config import token_settings


def _cookies(response: Response) -> list[str]:
    return response.headers.getlist('set-cookie')


def test_set_session_in_development_are_lax_and_not_secure(
    monkeypatch,
) -> None:
    monkeypatch.setattr(settings, 'env', 'development')
    response = Response()

    cookies.set_session(response, 'access-jwt', 'raw-refresh')

    header = _cookies(response)
    access = next(
        cookie for cookie in header if cookie.startswith(cookies.ACCESS_COOKIE_NAME)
    )
    refresh = next(
        cookie for cookie in header if cookie.startswith(cookies.REFRESH_COOKIE_NAME)
    )

    assert 'HttpOnly' in access
    assert 'HttpOnly' in refresh
    assert 'SameSite=lax' in access.lower() or 'samesite=lax' in access.lower()
    assert 'secure' not in access.lower().replace('samesite', '')
    assert f'Path={cookies.ACCESS_COOKIE_PATH}' in access
    assert f'Path={cookies.REFRESH_COOKIE_PATH}' in refresh
    assert f'Max-Age={token_settings.expiration_seconds}' in access
    assert f'Max-Age={token_settings.refresh_expiration_seconds}' in refresh


def test_set_session_in_production_are_strict_and_secure(
    monkeypatch,
) -> None:
    monkeypatch.setattr(settings, 'env', 'production')
    response = Response()

    cookies.set_session(response, 'access-jwt', 'raw-refresh')

    header = _cookies(response)
    access = next(
        cookie for cookie in header if cookie.startswith(cookies.ACCESS_COOKIE_NAME)
    )
    refresh = next(
        cookie for cookie in header if cookie.startswith(cookies.REFRESH_COOKIE_NAME)
    )

    assert 'Secure' in access
    assert 'Secure' in refresh
    assert 'samesite=strict' in access.lower()
    assert 'samesite=strict' in refresh.lower()
    assert f'Path={cookies.ACCESS_COOKIE_PATH}' in access
    assert f'Path={cookies.REFRESH_COOKIE_PATH}' in refresh


def test_clear_session_expires_both_paths() -> None:
    response = Response()

    cookies.clear_session(response)

    header = ''.join(_cookies(response))
    assert cookies.ACCESS_COOKIE_NAME in header
    assert cookies.REFRESH_COOKIE_NAME in header
    assert cookies.ACCESS_COOKIE_PATH in header
    assert cookies.REFRESH_COOKIE_PATH in header


def test_get_refresh_returns_the_refresh_cookie() -> None:
    request = Request({
        'type': 'http',
        'method': 'POST',
        'path': '/api/auth/session/refresh',
        'headers': [
            (
                b'cookie',
                f'{cookies.REFRESH_COOKIE_NAME}=raw-refresh'.encode(),
            )
        ],
        'query_string': b'',
    })

    assert cookies.get_refresh(request) == 'raw-refresh'


def test_get_refresh_returns_none_when_missing() -> None:
    request = Request({
        'type': 'http',
        'method': 'POST',
        'path': '/api/auth/session/refresh',
        'headers': [],
        'query_string': b'',
    })

    assert cookies.get_refresh(request) is None
