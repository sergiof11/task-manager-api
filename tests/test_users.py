def test_register_user(client):
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


def test_register_duplicate_email(client):
    user_data = {
        "email": "test@example.com",
        "password": "Password123"
    }

    client.post("/users/register", json=user_data)

    response = client.post("/users/register", json=user_data)

    assert response.status_code == 400
    assert response.json()["detail"] == "El email ya está registrado"


def test_register_invalid_email(client):
    response = client.post(
        "/users/register",
        json={
            "email": "email-invalido",
            "password": "Password123"
        }
    )

    assert response.status_code == 422