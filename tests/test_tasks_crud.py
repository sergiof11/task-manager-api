def test_get_tasks(client, auth_headers):
    response = client.get(
        "/tasks",
        headers=auth_headers,
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)


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
            "title": "Tarea de prueba",
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
            "title": "Tarea original",
        },
        headers=auth_headers,
    )

    task_id = create_response.json()["id"]

    response = client.put(
        f"/tasks/{task_id}",
        json={
            "title": "Tarea actualizada",
            "completed": True,
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
            "completed": True,
        },
        headers=auth_headers,
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Tarea no encontrada"


def test_get_task(client, auth_headers):
    create_response = client.post(
        "/tasks",
        json={
            "title": "Tarea para buscar",
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
            "title": "Tarea para eliminar",
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
            "title": "     ",
        },
        headers=auth_headers,
    )

    assert response.status_code == 422


def test_get_task_with_invalid_id(client, auth_headers):
    response = client.get(
        "/tasks/0",
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