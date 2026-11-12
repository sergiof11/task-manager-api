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