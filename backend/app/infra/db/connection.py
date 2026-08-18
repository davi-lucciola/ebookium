from sqlalchemy.ext.asyncio import create_async_engine

from app.infra.db.config import database_settings

engine = create_async_engine(
    database_settings.url,
    echo=database_settings.show_sql,
)
