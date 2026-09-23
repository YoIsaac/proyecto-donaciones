from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "API de Gestión de Donaciones activa"}


def test_login_exitoso():
    response = client.post(
        "/api/auth/login",
        json={"email": "admin@redsolidaria.org", "password": "PasswordSegura123!"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "token" in data
    assert data["role"] == "ADMIN"


def test_login_fallido():
    response = client.post(
        "/api/auth/login",
        json={"email": "admin@redsolidaria.org", "password": "PasswordIncorrecta"},
    )
    assert response.status_code == 401


def test_listar_donaciones_con_token():
    login_res = client.post(
        "/api/auth/login",
        json={"email": "admin@redsolidaria.org", "password": "PasswordSegura123!"},
    )
    token = login_res.json()["token"]

    response = client.get(
        "/api/donaciones",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    assert len(response.json()) >= 1


def test_crear_donacion_como_admin():
    login_res = client.post(
        "/api/auth/login",
        json={"email": "admin@redsolidaria.org", "password": "PasswordSegura123!"},
    )
    token = login_res.json()["token"]

    response = client.post(
        "/api/donaciones",
        json={"donante": "Walmart México", "tipo": "Granos", "cantidad_kg": 500.0},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 201
    assert response.json()["donante"] == "Walmart México"


def test_crear_donacion_denegado_para_usuario():
    login_res = client.post(
        "/api/auth/login",
        json={"email": "donante@empresa.com", "password": "Password123!"},
    )
    token = login_res.json()["token"]

    response = client.post(
        "/api/donaciones",
        json={"donante": "Empresa Pequeña", "tipo": "Lácteos", "cantidad_kg": 50.0},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 403
