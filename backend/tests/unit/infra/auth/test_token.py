from datetime import UTC, datetime, timedelta

import jwt
import pytest

from app.config import settings
from app.infra.auth import token
from app.infra.auth.config import token_settings


def test_create_token():
    claims = token.get_claims('davi@email.com')

    encoded = token.encode_token(claims)
    assert encoded is not None

    decoded = token.decode_token(encoded)

    assert decoded['sub'] == 'davi@email.com'
    assert decoded['iss'] == claims['iss']
    assert decoded['typ'] == 'access'
    assert 'exp' in decoded
    assert 'iat' in decoded
    assert 'jti' in decoded


def test_get_claims_stringifies_the_subject() -> None:
    """The JWT `sub` is always a string, but the service passes the integer `id`."""

    assert token.get_claims(42)['sub'] == '42'


def test_get_claims_uses_the_app_title_as_issuer() -> None:
    assert token.get_claims(1)['iss'] == settings.title


def test_get_claims_defaults_to_access_type() -> None:
    assert token.get_claims(1)['typ'] == 'access'


def test_get_claims_expires_according_to_the_settings() -> None:
    claims = token.get_claims(1)

    assert claims['exp'] - claims['iat'] == timedelta(
        seconds=token_settings.expiration_seconds
    )


def test_get_claims_refresh_uses_refresh_ttl() -> None:
    claims = token.get_claims(
        1,
        token_type='refresh',
        expiration_seconds=token_settings.refresh_expiration_seconds,
    )

    assert claims['typ'] == 'refresh'
    assert claims['exp'] - claims['iat'] == timedelta(
        seconds=token_settings.refresh_expiration_seconds
    )


def test_get_claims_includes_a_unique_jti() -> None:
    assert token.get_claims(1)['jti'] != token.get_claims(1)['jti']


def test_decode_an_expired_token_raises() -> None:
    claims = token.get_claims(1)
    claims['exp'] = datetime.now(UTC) - timedelta(seconds=1)

    with pytest.raises(jwt.ExpiredSignatureError):
        token.decode_token(token.encode_token(claims))


def test_decode_a_token_signed_with_another_secret_raises() -> None:
    forged = jwt.encode({'sub': '1'}, 'another-secret-long-enough-for-hs256')

    with pytest.raises(jwt.InvalidSignatureError):
        token.decode_token(forged)


def test_decode_a_malformed_token_raises() -> None:
    with pytest.raises(jwt.DecodeError):
        token.decode_token('not-a-jwt')
