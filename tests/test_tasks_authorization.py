import jwt

from app.config import settings
from app.database import SessionLocal
from app.models import TaskDB


def test_get_tasks_without_token(client):
    response = client.get("/tasks")

    assert response.status_code == 401
    assert response.json()["detail"] == "Token inválido o expirado"
    assert response.headers["www-authenticate"] == "Bearer"


def test_get_tasks_with_invalid_token(client):
    response = client.get(
        "/tasks",
        headers={
            "Authorization": "Bearer invalid-token",
        },
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Token inválido o expirado"
    assert response.headers["www-authenticate"] == "Bearer"


def test_created_task_belongs_to_authenticated_user(client, auth_headers):
    response = client.post(
        "/tasks",
        json={
            "title": "Tarea con propietario",
        },
        headers=auth_headers,
    )

    assert response.status_code == 201

    task_id = response.json()["id"]

    token = auth_headers["Authorization"].replace("Bearer ", "")

    payload = jwt.decode(
        token,
        settings.jwt_secret_key,
        algorithms=[settings.jwt_algorithm],
    )

    user_id = int(payload["sub"])

    db = SessionLocal()

    try:
        task = db.query(TaskDB).filter(TaskDB.id == task_id).first()

        assert task is not None
        assert task.user_id == user_id
    finally:
        db.close()


def test_users_only_list_their_own_tasks(
    client,
    auth_headers,
    second_auth_headers,
):
    client.post(
        "/tasks",
        json={"title": "Tarea usuario uno"},
        headers=auth_headers,
    )

    client.post(
        "/tasks",
        json={"title": "Tarea usuario dos"},
        headers=second_auth_headers,
    )

    response_user_one = client.get(
        "/tasks",
        headers=auth_headers,
    )

    response_user_two = client.get(
        "/tasks",
        headers=second_auth_headers,
    )

    assert response_user_one.status_code == 200
    assert response_user_two.status_code == 200

    assert len(response_user_one.json()) == 1
    assert len(response_user_two.json()) == 1

    assert response_user_one.json()[0]["title"] == "Tarea usuario uno"
    assert response_user_two.json()[0]["title"] == "Tarea usuario dos"


def test_user_cannot_get_another_users_task(
    client,
    auth_headers,
    second_auth_headers,
):
    create_response = client.post(
        "/tasks",
        json={"title": "Tarea privada"},
        headers=auth_headers,
    )

    task_id = create_response.json()["id"]

    response = client.get(
        f"/tasks/{task_id}",
        headers=second_auth_headers,
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Tarea no encontrada"


def test_user_cannot_update_another_users_task(
    client,
    auth_headers,
    second_auth_headers,
):
    create_response = client.post(
        "/tasks",
        json={"title": "Tarea privada"},
        headers=auth_headers,
    )

    task_id = create_response.json()["id"]

    response = client.put(
        f"/tasks/{task_id}",
        json={
            "title": "Intento de modificación",
            "completed": True,
        },
        headers=second_auth_headers,
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Tarea no encontrada"


def test_user_cannot_delete_another_users_task(
    client,
    auth_headers,
    second_auth_headers,
):
    create_response = client.post(
        "/tasks",
        json={"title": "Tarea privada"},
        headers=auth_headers,
    )

    task_id = create_response.json()["id"]

    response = client.delete(
        f"/tasks/{task_id}",
        headers=second_auth_headers,
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Tarea no encontrada"