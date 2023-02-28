"""This module contains pytest fixtures and configuration for the tests."""

import pytest

from src.app import app, db


@pytest.fixture
def client() -> app.test_client:
    """Return a test client for the Flask application."""
    app.config["TESTING"] = True
    client = app.test_client()

    with app.app_context():
        db.create_all()
        yield client
        db.drop_all()
