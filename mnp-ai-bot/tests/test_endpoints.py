import pytest
from starlette.testclient import TestClient
from app.main import app
from app.database import Base, engine, get_db
from app.auth import seed_initial_users

@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    Base.metadata.create_all(bind=engine)
    db = next(get_db())
    seed_initial_users(db)
    yield
    db.close()

def get_admin_token(client: TestClient) -> str:
    res = client.post("/auth/login", json={
        "olm_id": "OLM_ADMIN_001",
        "password": "Password@123"
    })
    assert res.status_code == 200
    return res.json()["access_token"]

def get_viewer_token(client: TestClient) -> str:
    res = client.post("/auth/login", json={
        "olm_id": "OLM_SUPPORT_001",
        "password": "Password@123"
    })
    assert res.status_code == 200
    return res.json()["access_token"]


def test_health_endpoint():
    """Verify system health probe and liveness."""
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data
    assert "environment" in data


def test_auth_login_success():
    """Verify OAuth2/JWT token generation on valid credentials."""
    client = TestClient(app)
    response = client.post("/auth/login", json={
        "olm_id": "OLM_ADMIN_001",
        "password": "Password@123"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["user"]["olm_id"] == "OLM_ADMIN_001"
    assert data["user"]["role"] == "admin"


def test_auth_login_invalid_password():
    """Verify rejection on incorrect password."""
    client = TestClient(app)
    response = client.post("/auth/login", json={
        "olm_id": "OLM_ADMIN_001",
        "password": "WrongPassword999"
    })
    assert response.status_code == 401
    assert "invalid olm credentials" in response.json()["detail"].lower()


def test_auth_login_nonexistent_user():
    """Verify rejection on non-existent OLM ID."""
    client = TestClient(app)
    response = client.post("/auth/login", json={
        "olm_id": "NON_EXISTENT_OLM_USER",
        "password": "Password@123"
    })
    assert response.status_code == 401


def test_auth_me_unauthorized():
    """Verify protected user route rejects requests missing Bearer tokens."""
    client = TestClient(app)
    response = client.get("/auth/me")
    assert response.status_code == 401


def test_auth_me_authorized():
    """Verify token identity resolution on /auth/me."""
    client = TestClient(app)
    token = get_admin_token(client)
    response = client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["olm_id"] == "OLM_ADMIN_001"


def test_analyze_unauthorized():
    """Verify /analyze cannot be accessed without valid credentials."""
    client = TestClient(app)
    response = client.post("/analyze", json={"msisdn": "919890123456"})
    assert response.status_code == 401


def test_analyze_authorized():
    """Verify end-to-end MNP journey analysis with JWT token."""
    client = TestClient(app)
    token = get_admin_token(client)
    
    # Initialize fresh sample data
    client.post("/test/insert_sample_data")
    
    response = client.post(
        "/analyze",
        headers={"Authorization": f"Bearer {token}"},
        json={"msisdn": "919890123456"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["msisdn"] == "919890123456"
    assert "tabular_journey" in data
    assert "logs_analysis" in data
    assert "suggestions" in data
    assert isinstance(data["suggestions"], list)


def test_trai_cooling_period_violation_detection():
    """Verify TRAI regulation: 10-day cooling period breach triggers a critical warning."""
    client = TestClient(app)
    token = get_admin_token(client)
    
    # Populate sample data containing the 2-day return violation
    client.post("/test/insert_sample_data")
    
    response = client.post(
        "/analyze",
        headers={"Authorization": f"Bearer {token}"},
        json={"msisdn": "919890123456"}
    )
    assert response.status_code == 200
    suggestions = response.json()["suggestions"]
    
    # Check that at least one critical warning flags the cooling period
    cooling_warnings = [
        s for s in suggestions
        if "cooling period" in s["suggestion"].lower() or "cooling period" in s["details"].lower()
    ]
    assert len(cooling_warnings) > 0, "Expected TRAI cooling period warning in suggestions"


def test_role_based_access_control():
    """Verify RBAC: 'viewer' role is blocked from /users, whereas 'admin' is granted access."""
    client = TestClient(app)
    viewer_token = get_viewer_token(client)
    admin_token = get_admin_token(client)
    
    # Viewer should be forbidden (403)
    res_viewer = client.get("/users", headers={"Authorization": f"Bearer {viewer_token}"})
    assert res_viewer.status_code == 403
    
    # Admin should be allowed (200)
    res_admin = client.get("/users", headers={"Authorization": f"Bearer {admin_token}"})
    assert res_admin.status_code == 200
    assert len(res_admin.json()) >= 4
