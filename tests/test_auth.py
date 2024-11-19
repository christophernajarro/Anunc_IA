import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from backend.main import app
from backend.common.database.database import Base, get_db
from backend.common.models.usuario import Usuario, Cuenta

# Crear una URL para la base de datos de prueba (en memoria)
TEST_DATABASE_URL = "sqlite:///:memory:"

# Crear el motor de la base de datos de prueba
test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool  # Asegura que la base de datos en memoria persista durante toda la sesión de prueba
)

# Crear una clase de sesión configurada para las pruebas
TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine
)

# Importar todos los modelos antes de crear las tablas
# Esto asegura que SQLAlchemy conozca todos los modelos
from backend.common.models.usuario import Usuario, Cuenta  # Asegúrate de importar todos los modelos necesarios

# Crear las tablas en la base de datos de prueba
Base.metadata.create_all(bind=test_engine)

# Fixture para sobrescribir la dependencia get_db
@pytest.fixture(scope="module")
def override_get_db():
    """
    Esta fixture reemplaza la dependencia `get_db` en la aplicación FastAPI para usar la base de datos de prueba.
    """
    try:
        # Crear una nueva sesión de la base de datos de prueba
        db = TestingSessionLocal()
        yield db
    finally:
        # Cerrar la sesión después de las pruebas
        db.close()

# Aplicar la sobrescritura de la dependencia
app.dependency_overrides[get_db] = override_get_db

# Crear una instancia de TestClient usando la aplicación FastAPI con la dependencia sobrescrita
client = TestClient(app)

# Fixture para simular Redis usando mocks
@pytest.fixture(autouse=True)
def mock_redis():
    """
    Esta fixture utiliza `unittest.mock` para simular las interacciones con Redis.
    """
    with patch("backend.services.auth_service.security.SessionManager") as MockSessionManager:
        # Crear una instancia simulada de SessionManager
        instance = MockSessionManager.return_value
        instance.store_jwt = AsyncMock()
        instance.get_jwt = AsyncMock()
        instance.delete_jwt = AsyncMock()
        yield instance

# Fixture para proporcionar datos de usuario de prueba
@pytest.fixture
def test_user():
    return {
        "nombre": "Test User",
        "email": "testuser@example.com",
        "password": "password123"
    }

# Prueba para registrar un nuevo usuario
def test_register_user(test_user):
    response = client.post("/auth/register", json=test_user)
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == test_user["email"]
    assert "id_usuario" in data

# Prueba para intentar registrar un usuario existente
def test_register_existing_user(test_user):
    # Registrar el usuario por primera vez
    response = client.post("/auth/register", json=test_user)
    assert response.status_code == 201

    # Intentar registrar el mismo usuario de nuevo
    response = client.post("/auth/register", json=test_user)
    assert response.status_code == 400
    assert response.json()["detail"] == "El email ya está registrado."

# Prueba para iniciar sesión con credenciales válidas
def test_login_user(test_user):
    # Registrar el usuario primero
    client.post("/auth/register", json=test_user)

    login_data = {
        "username": test_user["email"],
        "password": test_user["password"]
    }
    response = client.post("/auth/login", data=login_data)
    assert response.status_code == 200
    # Dependiendo de la implementación, ajusta la aserción
    # Aquí asumimos que devuelve un token de acceso
    assert "access_token" in response.json()

# Prueba para iniciar sesión con credenciales inválidas
def test_login_invalid_credentials():
    login_data = {
        "username": "nonexistent@example.com",
        "password": "wrongpassword"
    }
    response = client.post("/auth/login", data=login_data)
    assert response.status_code == 400
    assert response.json()["detail"] == "Credenciales inválidas."

# Prueba para cerrar sesión
def test_logout_user(test_user):
    # Registrar el usuario primero
    client.post("/auth/register", json=test_user)

    # Iniciar sesión para obtener la cookie de sesión
    login_data = {
        "username": test_user["email"],
        "password": test_user["password"]
    }
    login_response = client.post("/auth/login", data=login_data)
    assert login_response.status_code == 200
    session_id = login_response.cookies.get("session_id")
    assert session_id is not None

    # Cerrar sesión
    response = client.post("/auth/logout", cookies={"session_id": session_id})
    assert response.status_code == 200
    assert response.json()["message"] == "Sesión cerrada"

# Prueba para verificar una sesión válida
def test_check_session_valid(test_user):
    # Registrar el usuario primero
    client.post("/auth/register", json=test_user)

    # Iniciar sesión para obtener la cookie de sesión
    login_data = {
        "username": test_user["email"],
        "password": test_user["password"]
    }
    login_response = client.post("/auth/login", data=login_data)
    assert login_response.status_code == 200
    session_id = login_response.cookies.get("session_id")
    assert session_id is not None

    # Verificar la sesión válida
    response = client.get("/auth/check_session", cookies={"session_id": session_id})
    assert response.status_code == 200
    assert response.json()["message"] == "Sesión válida"
    assert response.json()["user"] == test_user["email"]

# Prueba para verificar una sesión inválida
def test_check_session_invalid():
    # Intentar verificar una sesión sin proporcionar la cookie de sesión
    response = client.get("/auth/check_session")
    assert response.status_code == 401
    assert response.json()["detail"] == "Credenciales no proporcionadas."