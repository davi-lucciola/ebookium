from unittest.mock import AsyncMock

import pytest
from sqlalchemy.exc import IntegrityError

from app.core.exceptions import ConflictException
from app.core.users.models import User
from app.core.users.schemas import UserIn
from app.core.users.services import UserService
from app.infra.auth import security


@pytest.fixture
def user_service(user_repository: AsyncMock) -> UserService:
    return UserService(repository=user_repository)


@pytest.fixture
def user_in() -> UserIn:
    return UserIn(name='Test User', email='davi@email.com', password='secret')


async def test_find_by_id_delegates_to_repository(
    user_service: UserService, user_repository: AsyncMock, user: User
) -> None:
    user_repository.find_by_id.return_value = user

    result = await user_service.find_by_id(user.id)

    assert result is user
    user_repository.find_by_id.assert_awaited_once_with(user.id)


async def test_find_by_email_delegates_to_repository(
    user_service: UserService, user_repository: AsyncMock, user: User
) -> None:
    user_repository.find_by_email.return_value = user

    result = await user_service.find_by_email(user.email)

    assert result is user
    user_repository.find_by_email.assert_awaited_once_with(user.email)


async def test_create_user_persists_the_new_user(
    user_service: UserService, user_repository: AsyncMock, user_in: UserIn, user: User
) -> None:
    user_repository.save.return_value = user

    result = await user_service.create(user_in)

    assert result is user
    saved = user_repository.save.await_args.args[0]
    assert saved.name == 'Test User'
    assert saved.email == 'davi@email.com'


async def test_create_user_hashes_the_password(
    user_service: UserService, user_repository: AsyncMock, user_in: UserIn
) -> None:
    await user_service.create(user_in)

    saved = user_repository.save.await_args.args[0]
    assert saved.password != 'secret'
    assert security.verify_password('secret', saved.password)


async def test_create_user_with_duplicated_email_raises_conflict(
    user_service: UserService, user_repository: AsyncMock, user_in: UserIn
) -> None:
    """The email is unique in the database: the repo IntegrityError becomes 409."""

    user_repository.save.side_effect = IntegrityError('stmt', {}, Exception())

    with pytest.raises(
        ConflictException, match='A user with this email already exists.'
    ):
        await user_service.create(user_in)
