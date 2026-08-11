import os

import pytest

os.environ.setdefault("FASTAPI_ENV", "development")

from fastapi.testclient import TestClient  # noqa: E402

from app.main import app  # noqa: E402


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)
