import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.database import Base
from app.core.dependencies import get_db
from app.main import app
from app.utils.enums import Role

# Use an isolated memory-mapped database string for test routines
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db_session():
    """Initializes schema tables cleanly before each test and drops them after execution."""
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(db_session):
    """Dynamic injection hook override supplying the isolated database session context."""
    def _get_test_db():
        try:
            yield db_session
        finally:
            pass
            
    app.dependency_overrides[get_db] = _get_test_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()

@pytest.fixture
def generate_token(monkeypatch):
    """Generates valid structural JWT access token payloads for test role authorization verification."""
    from jose import jwt
    from app.core.config import settings
    
    def _create_mock_token(user_id: str, role: str) -> str:
        # Enforce hardcoded secrets for testing environments safely
        monkeypatch.setattr(settings, "JWT_SECRET", "test_secret_key_1234567890_hackathon_demo")
        monkeypatch.setattr(settings, "ALGORITHM", "HS256")
        
        to_encode = {"sub": str(user_id), "role": role}
        return jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.ALGORITHM)
        
    return _create_mock_token