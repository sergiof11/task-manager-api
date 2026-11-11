import jwt

from app.config import settings
from app.database import SessionLocal
from app.models import TaskDB


def test_get_tasks(client, auth_headers):
    response = client.get(
        "/tasks",
        headers=auth_headers,
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)


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


def test_get_task_not_found(client, auth_headers):
    response = client.get(
        "/tasks/999999",
        headers=auth_headers,
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Tarea no encontrada"


def test_create_task(client, auth_headers):
    response = client.post(
        "/tasks",
        json={
            "title": "Tarea de prueba"
        },
        headers=auth_headers,
    )

    assert response.status_code == 201

    data = response.json()

    assert data["title"] == "Tarea de prueba"
    assert data["completed"] is False
    assert "id" in data


def test_update_task(client, auth_headers):
    create_response = client.post(
        "/tasks",
        json={
            "title": "Tarea original"
        },
        headers=auth_headers,
    )

    task_id = create_response.json()["id"]

    response = client.put(
        f"/tasks/{task_id}",
        json={
            "title": "Tarea actualizada",
            "completed": True
        },
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == task_id
    assert data["title"] == "Tarea actualizada"
    assert data["completed"] is True


def test_update_task_not_found(client, auth_headers):
    response = client.put(
        "/tasks/999999",
        json={
            "title": "No existe",
            "completed": True
        },
        headers=auth_headers,
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Tarea no encontrada"


def test_get_task(client, auth_headers):
    create_response = client.post(
        "/tasks",
        json={
            "title": "Tarea para buscar"
        },
        headers=auth_headers,
    )

    task_id = create_response.json()["id"]

    response = client.get(
        f"/tasks/{task_id}",
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == task_id
    assert data["title"] == "Tarea para buscar"
    assert data["completed"] is False


def test_delete_task(client, auth_headers):
    create_response = client.post(
        "/tasks",
        json={
            "title": "Tarea para eliminar"
        },
        headers=auth_headers,
    )

    task_id = create_response.json()["id"]

    response = client.delete(
        f"/tasks/{task_id}",
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["message"] == "Tarea eliminada"
    assert data["id"] == task_id
    assert data["title"] == "Tarea para eliminar"
    assert data["completed"] is False


def test_delete_task_not_found(client, auth_headers):
    response = client.delete(
        "/tasks/999999",
        headers=auth_headers,
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Tarea no encontrada"


def test_create_task_with_empty_title(client, auth_headers):
    response = client.post(
        "/tasks",
        json={
            "title": "     "
        },
        headers=auth_headers,
    )

    assert response.status_code == 422


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


def test_get_tasks_with_pagination(client, auth_headers):
    for number in range(5):
        client.post(
            "/tasks",
            json={"title": f"Tarea {number}"},
            headers=auth_headers,
        )

    response = client.get(
        "/tasks?skip=1&limit=2",
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2
    assert data[0]["title"] == "Tarea 1"
    assert data[1]["title"] == "Tarea 2"


def test_get_tasks_filter_completed_true(client, auth_headers):
    client.post(
        "/tasks",
        json={
            "title": "Pendiente",
            "completed": False,
        },
        headers=auth_headers,
    )

    client.post(
        "/tasks",
        json={
            "title": "Completada",
            "completed": True,
        },
        headers=auth_headers,
    )

    response = client.get(
        "/tasks?completed=true",
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["title"] == "Completada"
    assert data[0]["completed"] is True


def test_get_tasks_filter_completed_false(client, auth_headers):
    client.post(
        "/tasks",
        json={
            "title": "Pendiente",
            "completed": False,
        },
        headers=auth_headers,
    )

    client.post(
        "/tasks",
        json={
            "title": "Completada",
            "completed": True,
        },
        headers=auth_headers,
    )

    response = client.get(
        "/tasks?completed=false",
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["title"] == "Pendiente"
    assert data[0]["completed"] is False


def test_get_tasks_invalid_limit(client, auth_headers):
    response = client.get(
        "/tasks?limit=0",
        headers=auth_headers,
    )

    assert response.status_code == 422


def test_get_task_with_invalid_id(client, auth_headers):
    response = client.get(
        "/tasks/0",
        headers=auth_headers,
    )

    assert response.status_code == 422


def test_get_tasks_with_negative_skip(client, auth_headers):
    response = client.get(
        "/tasks?skip=-1",
        headers=auth_headers,
    )

    assert response.status_code == 422


def test_get_tasks_with_limit_over_maximum(client, auth_headers):
    response = client.get(
        "/tasks?limit=101",
        headers=auth_headers,
    )

    assert response.status_code == 422


def test_get_tasks_with_invalid_completed_filter(client, auth_headers):
    response = client.get(
        "/tasks?completed=invalid",
        headers=auth_headers,
    )

    assert response.status_code == 422


def test_create_task_with_title_too_long(client, auth_headers):
    response = client.post(
        "/tasks",
        json={
            "title": "a" * 201,
        },
        headers=auth_headers,
    )

    assert response.status_code == 422
