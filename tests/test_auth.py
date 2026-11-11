from datetime import UTC, datetime, timedelta

import jwt

from app.config import settings


def test_login_user(client):
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

    assert "access_token" in data
    assert isinstance(data["access_token"], str)
    assert data["token_type"] == "bearer"

    payload = jwt.decode(
        data["access_token"],
        settings.jwt_secret_key,
        algorithms=[settings.jwt_algorithm],
    )

    assert "sub" in payload
    assert "exp" in payload


def test_login_wrong_password(client):
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
    assert response.headers["www-authenticate"] == "Bearer"


def test_login_user_not_found(client):
    response = client.post(
        "/auth/login",
        json={
            "email": "doesnotexist@example.com",
            "password": "Password123",
        },
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Email o contraseña incorrectos"
    assert response.headers["www-authenticate"] == "Bearer"


def test_get_current_user(client):
    client.post(
        "/users/register",
        json={
            "email": "me@example.com",
            "password": "Password123",
        },
    )

    login_response = client.post(
        "/auth/login",
        json={
            "email": "me@example.com",
            "password": "Password123",
        },
    )

    access_token = login_response.json()["access_token"]

    response = client.get(
        "/auth/me",
        headers={
            "Authorization": f"Bearer {access_token}",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["email"] == "me@example.com"
    assert "password" not in data
    assert "hashed_password" not in data


def test_get_current_user_with_invalid_token(client):
    response = client.get(
        "/auth/me",
        headers={
            "Authorization": "Bearer invalid-token",
        },
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Token inválido o expirado"
    assert response.headers["www-authenticate"] == "Bearer"


def test_get_current_user_with_expired_token(client):
    expired_token = jwt.encode(
        {
            "sub": "1",
            "exp": datetime.now(UTC) - timedelta(minutes=1),
        },
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
    )

    response = client.get(
        "/auth/me",
        headers={
            "Authorization": f"Bearer {expired_token}",
        },
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Token inválido o expirado"
    assert response.headers["www-authenticate"] == "Bearer"


def test_login_with_password_too_long(client):
    response = client.post(
        "/auth/login",
        json={
            "email": "test@example.com",
            "password": "a" * 129,
        },
    )

    assert response.status_code == 422


def test_get_current_user_with_nonexistent_user(client):
    token = jwt.encode(
        {
            "sub": "999999",
            "exp": datetime.now(UTC) + timedelta(minutes=5),
        },
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
    )

    response = client.get(
        "/auth/me",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Token inválido o expirado"
    assert response.headers["www-authenticate"] == "Bearer"
