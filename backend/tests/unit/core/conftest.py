"""Session fixture for repository unit tests.

Unit tests do not open a database. SQLAlchemy repositories receive a mocked
`AsyncSession` and the contract with it is what is asserted: which method was
called, with which object, and how the session return is passed through.
"""

from unittest.mock import AsyncMock

import pytest
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.fixture
def db() -> AsyncMock:
    return AsyncMock(spec=AsyncSession)
