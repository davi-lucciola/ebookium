import os

os.environ.setdefault('APP_ENV', 'development')
os.environ.setdefault('APP_TOKEN_SECRET', 'test-secret-test-secret-test-sec')
os.environ.setdefault(
    'APP_DATABASE_URL',
    'postgresql+psycopg://unused:unused@localhost:5432/unused',
)

from collections.abc import Iterator

import pytest
from pwdlib import PasswordHash
from pwdlib.hashers.bcrypt import BcryptHasher

from app.infra.auth import security

# --------------------------------------------------------------------------- #
# cheap bcrypt
# --------------------------------------------------------------------------- #
# UserService hashes the password on create, and fixtures that persist a user
# call security.hash_password explicitly — so any test that depends on a user
# pays a full bcrypt. With the default cost (12 rounds) that is ~300ms per
# test, enough to dominate the suite.
#
# 4 is the minimum cost bcrypt accepts: the algorithm, salt and hash format
# stay the same, only the work factor drops. What the tests check (hash !=
# password, different salts, verify matches) does not depend on the cost.

_CHEAP_PWD_CONTEXT = PasswordHash((BcryptHasher(rounds=4),))


@pytest.fixture(autouse=True, scope='session')
def _cheap_password_hashing() -> Iterator[None]:
    original = security.pwd_context
    security.pwd_context = _CHEAP_PWD_CONTEXT
    yield
    security.pwd_context = original


# --------------------------------------------------------------------------- #
# automatic markers
# --------------------------------------------------------------------------- #
# Each test gets two markers derived from the file path: the suite
# (`unit`/`integration`) and the domain (`auth`, `users`, ...). That avoids
# repeating `pytestmark` in every file and keeps markers correct when a test
# moves folders. Names must be registered in `pyproject.toml` because
# `--strict-markers` is on.

_LAYER_DIRS = frozenset({'api', 'core'})


def _markers_for(parts: tuple[str, ...]) -> tuple[str, ...]:
    """('unit', 'core', 'users', 'test_x.py') -> ('unit', 'users')."""
    suite = parts[0]
    rest = parts[1:-1]  # directories between the suite and the file

    if suite == 'unit' and rest[:1] and rest[0] in _LAYER_DIRS:
        rest = rest[1:]

    if not rest:
        return (suite,)

    return (suite, rest[0])


def pytest_collection_modifyitems(
    config: pytest.Config, items: list[pytest.Item]
) -> None:
    tests_root = config.rootpath / 'tests'

    for item in items:
        parts = item.path.relative_to(tests_root).parts
        for marker in _markers_for(parts):
            item.add_marker(marker)
