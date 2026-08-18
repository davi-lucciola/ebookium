"""Shared fixtures for unit tests.

Two families:

- **external dependency mocks** — one `AsyncMock(spec=<Class>)` per repository.
  The `spec` is what makes the test break when the class changes, instead of
  the mock silently accepting a dead call.
- **in-memory entities** — real model instances with `id` assigned by hand.
  They never go through the database: services only read attributes and call
  domain methods, so a loose instance is enough.
"""

from datetime import datetime, timezone
from unittest.mock import AsyncMock

import pytest

from app.core.users.models import User
from app.core.users.repositories import UserRepository
from app.infra.auth import security

NOW = datetime(2025, 5, 28, tzinfo=timezone.utc)


@pytest.fixture
def user_repository() -> AsyncMock:
    return AsyncMock(spec=UserRepository)


@pytest.fixture
def user() -> User:
    user = User(
        name='Test User',
        email='davi@email.com',
        password=security.hash_password('secret'),
    )
    user.id = 1
    user.created_at = NOW
    user.updated_at = NOW
    return user
