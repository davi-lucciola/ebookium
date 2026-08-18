import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.users.models import User
from app.infra.auth import security


@pytest.fixture
async def test_user(test_db: AsyncSession) -> User:
    user = User(
        name='test',
        email='davi@email.com',
        password=security.hash_password('test'),
    )
    test_db.add(user)
    await test_db.commit()
    return user
