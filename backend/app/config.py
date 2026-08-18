from pathlib import Path
from typing import Any

from pydantic_settings import BaseSettings, SettingsConfigDict

# backend/app/config.py -> parents: app, backend
_ENV_FILE_PATH = Path(__file__).resolve().parent.parent / '.env'
ENV_FILE = _ENV_FILE_PATH if _ENV_FILE_PATH.is_file() else None


def app_settings_config(env_prefix: str) -> SettingsConfigDict:
    config: dict[str, Any] = {'env_prefix': env_prefix, 'extra': 'ignore'}
    if ENV_FILE is not None:
        config['env_file'] = ENV_FILE
    return SettingsConfigDict(**config)


class Settings(BaseSettings):
    model_config = app_settings_config('APP_')

    env: str = 'production'
    title: str = 'Ebookium API'


settings = Settings()
