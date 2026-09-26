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
