from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.infra.db.connection import engine


async def get_db():
    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session


Session = Annotated[AsyncSession, Depends(get_db)]
