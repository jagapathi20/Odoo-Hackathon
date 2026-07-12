from typing import List
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import sessionmaker  # Assumes a session provider setup
from app.models.user import User
from app.utils.enums import Role

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

def get_db():
    """Database session generator dependency."""
    db = sessionmaker()
    try:
        yield db
    finally:
        db.close()

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    """
    Extracts, decodes, and validates the incoming JWT token.
    Returns the current authenticated user record.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
        
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise credentials_exception
        
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Account is inactive"
        )
        
    return user

class RoleChecker:
    """
    Dynamic dependency class to guard routes by allowed roles.
    Enforces server-side permission validation.
    """
    def __init__(self, allowed_roles: List[Role]):
        self.allowed_roles = allowed_roles

    def __call__(self, current_user: User = Depends(get_current_user)):
        if current_user.role not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Role not permitted to access this resource"
            )
        return current_user

# Pre-defined convenience guards for endpoints
require_admin = RoleChecker([Role.ADMIN])
require_asset_manager = RoleChecker([Role.ADMIN, Role.ASSET_MANAGER])
require_management = RoleChecker([Role.ADMIN, Role.ASSET_MANAGER, Role.DEPARTMENT_HEAD])