from typing import Literal, TypedDict

from fastapi import Request, Response

from app.config import settings
from app.infra.auth.config import token_settings

ACCESS_COOKIE_NAME = 'access_token'
REFRESH_COOKIE_NAME = 'refresh_token'
ACCESS_COOKIE_PATH = '/api'
REFRESH_COOKIE_PATH = '/api/auth'


class CookieFlags(TypedDict):
    httponly: bool
    secure: bool
    samesite: Literal['lax', 'strict']


def _cookie_flags() -> CookieFlags:
    if settings.env == 'development':
        return CookieFlags(httponly=True, secure=False, samesite='lax')

    return CookieFlags(httponly=True, secure=True, samesite='strict')


def get_refresh(request: Request) -> str | None:
    return request.cookies.get(REFRESH_COOKIE_NAME)


def set_session(response: Response, access_token: str, refresh_token: str) -> None:
    flags = _cookie_flags()
    response.set_cookie(
        ACCESS_COOKIE_NAME,
        access_token,
        path=ACCESS_COOKIE_PATH,
        max_age=token_settings.expiration_seconds,
        **flags,
    )
    response.set_cookie(
        REFRESH_COOKIE_NAME,
        refresh_token,
        path=REFRESH_COOKIE_PATH,
        max_age=token_settings.refresh_expiration_seconds,
        **flags,
    )


def clear_session(response: Response) -> None:
    response.delete_cookie(ACCESS_COOKIE_NAME, path=ACCESS_COOKIE_PATH)
    response.delete_cookie(REFRESH_COOKIE_NAME, path=REFRESH_COOKIE_PATH)
