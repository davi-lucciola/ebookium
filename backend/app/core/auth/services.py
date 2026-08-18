from dataclasses import dataclass

import jwt

from app.core.exceptions import AuthenticationError
from app.core.users.models import User
from app.core.users.services import UserService
from app.infra.auth import security, token
from app.infra.auth.config import token_settings
from app.infra.auth.token import TokenType


@dataclass
class AuthService:
    user_service: UserService

    async def authenticate(self, access_token: str) -> User:
        payload = self._decode(access_token, expected_type='access')
        user = await self.user_service.find_by_id(int(payload['sub']))

        if user is None or not user.is_active:
            raise AuthenticationError('User not found.')

        return user

    async def login(self, email: str, password: str) -> User:
        user = await self.user_service.find_by_email(email)

        if not user or not security.verify_password(password, user.password):
            raise AuthenticationError('Invalid credentials.')

        return user

    @staticmethod
    def issue_session(user: User) -> tuple[str, str]:
        access_token = token.encode_token(
            token.get_claims(user.id, token_type='access')
        )
        refresh_token = token.encode_token(
            token.get_claims(
                user.id,
                token_type='refresh',
                expiration_seconds=token_settings.refresh_expiration_seconds,
            )
        )
        return access_token, refresh_token

    async def rotate_session(self, refresh_token: str) -> tuple[User, str, str]:
        payload = self._decode(refresh_token, expected_type='refresh')
        user = await self.user_service.find_by_id(int(payload['sub']))

        if user is None or not user.is_active:
            raise AuthenticationError('User not found.')

        access_token, new_refresh = self.issue_session(user)
        return user, access_token, new_refresh

    @staticmethod
    def _decode(raw: str, expected_type: TokenType) -> token.JWTClaims:
        try:
            payload = token.decode_token(raw)
        except jwt.ExpiredSignatureError:
            raise AuthenticationError('Expired token.') from None
        except jwt.PyJWTError:
            raise AuthenticationError('Invalid token.') from None

        if payload.get('typ') != expected_type:
            raise AuthenticationError('Invalid token.')

        return payload
