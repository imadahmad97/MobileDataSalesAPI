# tests/conftest.py
import pytest
from app.service.db_service import DataBaseService


@pytest.fixture
def db_service():
    # In-memory SQLite for testing
    service = DataBaseService("sqlite:///:memory:")
    service.create_db_and_tables()
    return service
