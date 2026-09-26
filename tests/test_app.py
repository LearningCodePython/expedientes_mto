import os
import tempfile
import pytest
from app import app, init_db, DB_PATH

@pytest.fixture
def client():
    # Use a temporary database for testing
    db_fd, db_path = tempfile.mkstemp()
    app.config["TESTING"] = True
    
    # Temporarily override DB_PATH in app module and db_service
    import app as app_module
    import services.db_service as db_service
    original_db_path = db_service.DB_PATH
    db_service.DB_PATH = db_path
    app_module.DB_PATH = db_path
    
    # Initialize test database
    init_db()
    
    with app.test_client() as client:
        yield client
        
    os.close(db_fd)
    os.unlink(db_path)
    db_service.DB_PATH = original_db_path
    app_module.DB_PATH = original_db_path

def test_index(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"<!DOCTYPE html>" in response.data or b"<html" in response.data

def test_check_auth_unauthenticated(client):
    response = client.get("/api/check-auth")
    assert response.status_code == 200
    data = response.get_json()
    assert data["authenticated"] is False

def test_login_success(client):
    response = client.post("/api/login", json={
        "username": "admin",
        "password": "admin123"
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "success"
    assert data["username"] == "admin"
    assert data["role"] == "admin"

def test_login_failure(client):
    response = client.post("/api/login", json={
        "username": "admin",
        "password": "wrongpassword"
    })
    assert response.status_code == 401
    data = response.get_json()
    assert "error" in data

def test_protected_endpoint_unauthorized(client):
    response = client.get("/api/data")
    assert response.status_code == 401

def test_get_and_save_data_authenticated(client):
    # Login first
    client.post("/api/login", json={
        "username": "admin",
        "password": "admin123"
    })
    
    # Get data
    response = client.get("/api/data")
    assert response.status_code == 200
    data = response.get_json()
    assert "company" in data
    assert "racks" in data
    assert len(data["racks"]) > 0
    
    # Save modified data
    company_data = data["company"]
    company_data["name"] = "Soportia Test Updated"
    racks_data = data["racks"]
    
    save_response = client.post("/api/data", json={
        "company": company_data,
        "racks": racks_data
    })
    assert save_response.status_code == 200
    assert save_response.get_json()["status"] == "success"
    
    # Verify update
    verify_response = client.get("/api/data")
    assert verify_response.get_json()["company"]["name"] == "Soportia Test Updated"

def test_change_password(client):
    # Login
    client.post("/api/login", json={
        "username": "admin",
        "password": "admin123"
    })
    
    # Change password
    res = client.post("/api/change-password", json={
        "current_password": "admin123",
        "new_password": "newsecure123"
    })
    assert res.status_code == 200
    assert res.get_json()["status"] == "success"
    
    # Logout
    client.post("/api/logout")
    
    # Try login with old password (should fail)
    res_old = client.post("/api/login", json={
        "username": "admin",
        "password": "admin123"
    })
    assert res_old.status_code == 401
    
    # Login with new password (should succeed)
    res_new = client.post("/api/login", json={
        "username": "admin",
        "password": "newsecure123"
    })
    assert res_new.status_code == 200

def test_admin_create_and_use_readonly_user(client):
    # Login as admin
    client.post("/api/login", json={
        "username": "admin",
        "password": "admin123"
    })
    
    # Create read-only user
    res = client.post("/api/users", json={
        "username": "viewer",
        "password": "viewer123",
        "role": "readonly"
    })
    assert res.status_code == 200
    assert res.get_json()["status"] == "success"
    
    # List users
    users_res = client.get("/api/users")
    assert users_res.status_code == 200
    users_list = users_res.get_json()["users"]
    assert any(u["username"] == "viewer" and u["role"] == "readonly" for u in users_list)
    
    # Logout admin
    client.post("/api/logout")
    
    # Login as viewer
    viewer_login = client.post("/api/login", json={
        "username": "viewer",
        "password": "viewer123"
    })
    assert viewer_login.status_code == 200
    assert viewer_login.get_json()["role"] == "readonly"
    
    # Viewer can read data
    get_res = client.get("/api/data")
    assert get_res.status_code == 200
    
    # Viewer cannot save data (should be 403 Forbidden)
    save_res = client.post("/api/data", json=get_res.get_json())
    assert save_res.status_code == 403
    
    # Viewer cannot create users (should be 403 Forbidden)
    create_res = client.post("/api/users", json={
        "username": "hacker",
        "password": "password",
        "role": "admin"
    })
    assert create_res.status_code == 403
