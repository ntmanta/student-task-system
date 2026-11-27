import pytest

from src.presentation.api import create_app


@pytest.fixture
def client():
    """A fresh app with an empty in-memory database for every test."""
    app = create_app(":memory:")
    app.config["TESTING"] = True
    return app.test_client()
