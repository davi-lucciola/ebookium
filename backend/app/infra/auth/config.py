from pydantic_settings import BaseSettings

from app.config import app_settings_config


class TokenSettings(BaseSettings):
    model_config = app_settings_config('APP_TOKEN_')

    secret: str
    algorithm: str = 'HS256'
    expiration_seconds: int = 3600
    refresh_expiration_seconds: int = 60 * 60 * 24 * 7


token_settings = TokenSettings()
