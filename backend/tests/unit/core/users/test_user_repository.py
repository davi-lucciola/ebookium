from unittest.mock import AsyncMock

import pytest

from app.core.users.models import User
from app.core.users.repositories import UserRepository


@pytest.fixture
def repository(db: AsyncMock) -> UserRepository:
    return UserRepository(db=db)


async def test_save_adds_a_new_user(
    repository: UserRepository, db: AsyncMock, user: User
) -> None:
    user.id = None  # type: ignore[assignment]

    assert await repository.save(user) is user
    db.add.assert_called_once_with(user)
    db.commit.assert_awaited_once()


async def test_save_does_not_re_add_a_persisted_user(
    repository: UserRepository, db: AsyncMock, user: User
) -> None:
    """Saving an entity already in the session is an update — adding again is noise."""

    await repository.save(user)

    db.add.assert_not_called()
    db.commit.assert_awaited_once()


async def test_find_by_id_returns_the_user(
    repository: UserRepository, db: AsyncMock, user: User
) -> None:
    db.scalar.return_value = user

    assert await repository.find_by_id(user.id) is user
    db.scalar.assert_awaited_once()


async def test_find_by_id_returns_none_when_missing(
    repository: UserRepository, db: AsyncMock
) -> None:
    db.scalar.return_value = None

    assert await repository.find_by_id(999) is None


async def test_find_by_email_returns_the_user(
    repository: UserRepository, db: AsyncMock, user: User
) -> None:
    db.scalar.return_value = user

    assert await repository.find_by_email('davi@email.com') is user
    db.scalar.assert_awaited_once()


async def test_find_by_email_returns_none_when_missing(
    repository: UserRepository, db: AsyncMock
) -> None:
    db.scalar.return_value = None

    assert await repository.find_by_email('ghost@email.com') is None
