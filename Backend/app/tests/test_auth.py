import pytest
import uuid
from fastapi import status
from app.models.user import User
from app.utils.enums import Role

def test_signup_always_enforces_employee_role(client, db_session):
    """Verifies that public signups hardcode the default EMPLOYEE role[cite: 31]."""
    dept_id = str(uuid.uuid4())
    
    payload = {
        "name": "Priya Shah",
        "email": "priya@company.com",
        "password": "securepassword123",
        "department_id": dept_id
    }
    
    # Try sending an explicit request to the signup endpoint [cite: 27]
    response = client.post("/api/v1/auth/signup", json=payload)
    
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["role"] == Role.EMPLOYEE.value  # Core server-side protection rule [cite: 31]
    assert data["email"] == "priya@company.com"

    # Verify database insertion
    db_user = db_session.query(User).filter(User.email == "priya@company.com").first()
    assert db_user is not None
    assert db_user.role == Role.EMPLOYEE  # Confirm it persists safely in the DB [cite: 31]


def test_login_blocks_inactive_users(client, db_session):
    """Ensures that accounts flagged as INACTIVE are rejected at authentication[cite: 33]."""
    from app.core.security import hash_password
    
    # Register an inactive employee row [cite: 48]
    inactive_user = User(
        id=uuid.uuid4(),
        name="John Doe",
        email="john@company.com",
        hashed_password=hash_password("password123"),
        role=Role.EMPLOYEE,
        department_id=uuid.uuid4(),
        is_active=False  # Simulates status: INACTIVE [cite: 48]
    )
    db_session.add(inactive_user)
    db_session.commit()
    
    # Form submission matching OAuth2PasswordRequestForm rules
    login_payload = {
        "username": "john@company.com",
        "password": "password123"
    }
    
    response = client.post("/api/v1/auth/login", data=login_payload)
    
    # Must reject with 403 Forbidden per specifications
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert "Account is inactive" in response.json()["detail"]


def test_forgot_password_avoids_user_existence_leak(client):
    """Checks that the forgot-password flow yields an identical generic message[cite: 33]."""
    response = client.post("/api/v1/auth/forgot-password?email=nonexistent@company.com")
    
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"detail": "If this email exists, a reset link has been sent."}