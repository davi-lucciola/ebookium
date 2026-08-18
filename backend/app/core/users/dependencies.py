from typing import Annotated

from fastapi import Depends

from app.core.users.repositories import UserRepository as SQLAlchemyUserRepository
from app.core.users.services import UserService as UserServiceImpl
from app.infra.db import Session


def get_user_repository(db: Session) -> SQLAlchemyUserRepository:
    return SQLAlchemyUserRepository(db)


UserRepository = Annotated[SQLAlchemyUserRepository, Depends(get_user_repository)]


def get_user_service(repository: UserRepository) -> UserServiceImpl:
    return UserServiceImpl(repository=repository)


UserService = Annotated[UserServiceImpl, Depends(get_user_service)]
