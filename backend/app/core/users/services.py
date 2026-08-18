from dataclasses import dataclass

from sqlalchemy.exc import IntegrityError

from app.core.exceptions import ConflictException
from app.core.users.models import User
from app.core.users.repositories import UserRepository
from app.core.users.schemas import UserIn
from app.infra.auth import security


@dataclass
class UserService:
    repository: UserRepository

    async def find_by_id(self, id: int) -> User | None:
        return await self.repository.find_by_id(id)

    async def find_by_email(self, email: str) -> User | None:
        return await self.repository.find_by_email(email)

    async def create(self, user_in: UserIn) -> User:
        try:
            user = User(
                name=user_in.name,
                email=user_in.email,
                password=security.hash_password(user_in.password),
            )
            return await self.repository.save(user)
        except IntegrityError:
            raise ConflictException('A user with this email already exists.') from None
