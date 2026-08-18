from pydantic_settings import BaseSettings

from app.config import app_settings_config


class DatabaseSettings(BaseSettings):
    model_config = app_settings_config('APP_DATABASE_')

    url: str
    show_sql: bool = False


database_settings = DatabaseSettings()
