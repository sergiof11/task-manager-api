import os

os.environ["DB_NAME"] = "gestor_tareas_test"

from fastapi.testclient import TestClient

from app.database import SessionLocal
from app.main import app
from app.models import TaskDB, UserDB

client = TestClient(app)


def clear_tasks():
    db = SessionLocal()

    try:
        db.query(TaskDB).delete()
        db.commit()
    finally:
        db.close()


def test_get_tasks():
    clear_tasks()

    response = client.get("/tasks")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_task_not_found():
    clear_tasks()

    response = client.get("/tasks/999999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Tarea no encontrada"


def test_create_task():
    clear_tasks()

    response = client.post(
        "/tasks",
        json={
            "title": "Tarea de prueba"
        }
    )

    assert response.status_code == 201

    data = response.json()

    assert data["title"] == "Tarea de prueba"
    assert data["completed"] is False
    assert "id" in data


def test_update_task():
    clear_tasks()

    create_response = client.post(
        "/tasks",
        json={
            "title": "Tarea original"
        }
    )

    task_id = create_response.json()["id"]

    response = client.put(
        f"/tasks/{task_id}",
        json={
            "title": "Tarea actualizada",
            "completed": True
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == task_id
    assert data["title"] == "Tarea actualizada"
    assert data["completed"] is True


def test_update_task_not_found():
    clear_tasks()

    response = client.put(
        "/tasks/999999",
        json={
            "title": "No existe",
            "completed": True
        }
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Tarea no encontrada"


def test_get_task():
    clear_tasks()

    create_response = client.post(
        "/tasks",
        json={
            "title": "Tarea para buscar"
        }
    )

    task_id = create_response.json()["id"]

    response = client.get(f"/tasks/{task_id}")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == task_id
    assert data["title"] == "Tarea para buscar"
    assert data["completed"] is False


def test_delete_task():
    clear_tasks()

    create_response = client.post(
        "/tasks",
        json={
            "title": "Tarea para eliminar"
        }
    )

    task_id = create_response.json()["id"]

    response = client.delete(f"/tasks/{task_id}")

    assert response.status_code == 200

    data = response.json()

    assert data["message"] == "Tarea eliminada"
    assert data["id"] == task_id
    assert data["title"] == "Tarea para eliminar"
    assert data["completed"] is False


def test_delete_task_not_found():
    clear_tasks()

    response = client.delete("/tasks/999999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Tarea no encontrada"


def test_create_task_with_empty_title():
    clear_tasks()

    response = client.post(
        "/tasks",
        json={
            "title": "     "
        }
    )

    assert response.status_code == 422


def clear_users():
    db = SessionLocal()

    try:
        db.query(UserDB).delete()
        db.commit()
    finally:
        db.close()


def test_register_user():
    clear_users()

    response = client.post(
        "/users/register",
        json={
            "email": "test@example.com",
            "password": "Password123"
        }
    )

    assert response.status_code == 201

    data = response.json()

    assert "id" in data
    assert data["email"] == "test@example.com"
    assert "password" not in data
    assert "hashed_password" not in data


def test_register_duplicate_email():
    clear_users()

    user_data = {
        "email": "test@example.com",
        "password": "Password123"
    }

    client.post("/users/register", json=user_data)

    response = client.post("/users/register", json=user_data)

    assert response.status_code == 400
    assert response.json()["detail"] == "El email ya está registrado"


def test_register_invalid_email():
    clear_users()

    response = client.post(
        "/users/register",
        json={
            "email": "email-invalido",
            "password": "Password123"
        }
    )

    assert response.status_code == 422


def test_login_user():
    clear_users()

    client.post(
        "/users/register",
        json={
            "email": "login@example.com",
            "password": "Password123",
        },
    )

    response = client.post(
        "/auth/login",
        json={
            "email": "login@example.com",
            "password": "Password123",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["email"] == "login@example.com"
    assert "password" not in data
    assert "hashed_password" not in data


def test_login_wrong_password():
    clear_users()

    client.post(
        "/users/register",
        json={
            "email": "login@example.com",
            "password": "Password123",
        },
    )

    response = client.post(
        "/auth/login",
        json={
            "email": "login@example.com",
            "password": "WrongPassword",
        },
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Email o contraseña incorrectos"


def test_login_user_not_found():
    clear_users()

    response = client.post(
        "/auth/login",
        json={
            "email": "doesnotexist@example.com",
            "password": "Password123",
        },
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Email o contraseña incorrectos"
