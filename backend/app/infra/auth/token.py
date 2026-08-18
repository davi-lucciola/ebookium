import secrets
from datetime import UTC, datetime, timedelta
from typing import Any, Literal, TypedDict, cast

import jwt

from app.config import settings
from app.infra.auth.config import token_settings

TokenType = Literal['access', 'refresh']


class JWTClaims(TypedDict):
    iss: str
    sub: str
    exp: datetime
    iat: datetime
    typ: TokenType
    jti: str


def encode_token(payload: JWTClaims) -> str:
    return jwt.encode(
        cast(dict[str, Any], payload),
        token_settings.secret,
        token_settings.algorithm,
    )


def decode_token(token: str) -> JWTClaims:
    return JWTClaims(
        **jwt.decode(
            token,
            token_settings.secret,
            algorithms=[token_settings.algorithm],
        )
    )


def get_claims(
    sub: Any,
    *,
    token_type: TokenType = 'access',
    expiration_seconds: int | None = None,
) -> JWTClaims:
    ttl = (
        token_settings.expiration_seconds
        if expiration_seconds is None
        else expiration_seconds
    )
    initiated_at = datetime.now(UTC)
    expires_in = initiated_at + timedelta(seconds=ttl)

    return JWTClaims(
        sub=str(sub),
        iss=settings.title,
        exp=expires_in,
        iat=initiated_at,
        typ=token_type,
        jti=secrets.token_urlsafe(16),
    )
