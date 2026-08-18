from dataclasses import dataclass

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.users.models import User


@dataclass
class UserRepository:
    db: AsyncSession

    async def save(self, user: User) -> User:
        if getattr(user, 'id', None) is None:
            self.db.add(user)

        await self.db.commit()
        return user

    async def find_by_id(self, id: int) -> User | None:
        query = select(User).where(User.id == id)
        return await self.db.scalar(query)

    async def find_by_email(self, email: str) -> User | None:
        query = select(User).where(User.email == email)
        return await self.db.scalar(query)
