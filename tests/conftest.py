import os

os.environ["DB_NAME"] = "gestor_tareas_test"

import pytest
from fastapi.testclient import TestClient

from app.database import SessionLocal
from app.main import app
from app.models import TaskDB, UserDB


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture(autouse=True)
def clean_database():
    db = SessionLocal()

    try:
        db.query(TaskDB).delete()
        db.query(UserDB).delete()
        db.commit()
    finally:
        db.close()