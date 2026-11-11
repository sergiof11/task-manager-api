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


@pytest.fixture
def auth_headers(client):
    client.post(
        "/users/register",
        json={
            "email": "tasks@example.com",
            "password": "Password123",
        },
    )

    login_response = client.post(
        "/auth/login",
        json={
            "email": "tasks@example.com",
            "password": "Password123",
        },
    )

    access_token = login_response.json()["access_token"]

    return {
        "Authorization": f"Bearer {access_token}",
    }


@pytest.fixture(autouse=True)
def clean_database():
    db = SessionLocal()

    try:
        db.query(TaskDB).delete()
        db.query(UserDB).delete()
        db.commit()
    finally:
        db.close()


@pytest.fixture
def second_auth_headers(client):
    client.post(
        "/users/register",
        json={
            "email": "second@example.com",
            "password": "Password123",
        },
    )

    login_response = client.post(
        "/auth/login",
        json={
            "email": "second@example.com",
            "password": "Password123",
        },
    )

    access_token = login_response.json()["access_token"]

    return {
        "Authorization": f"Bearer {access_token}",
    }
