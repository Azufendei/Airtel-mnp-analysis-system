from datetime import datetime, timedelta
from typing import Optional, List
import bcrypt
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.models import UserOLM
from app.config import Config
from app.database import get_db

security = HTTPBearer(auto_error=False)

DEFAULT_INITIAL_PASSWORD = "Password@123"

def get_password_hash(password: str) -> str:
    # Truncate at 72 bytes as per bcrypt specification
    pwd_bytes = password.encode('utf-8')[:72]
    return bcrypt.hashpw(pwd_bytes, bcrypt.gensalt()).decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    if not hashed_password:
        return False
    try:
        pwd_bytes = plain_password.encode('utf-8')[:72]
        hash_bytes = hashed_password.encode('utf-8')
        return bcrypt.checkpw(pwd_bytes, hash_bytes)
    except Exception:
        return False

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=Config.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, Config.SECRET_KEY, algorithm=Config.ALGORITHM)

def authenticate_user(db: Session, olm_id: str, password: str) -> Optional[UserOLM]:
    user = db.query(UserOLM).filter(
        UserOLM.olm_id == olm_id,
        UserOLM.is_active == True
    ).first()
    
    if not user:
        return None
    
    # Verify password against hash
    if not verify_password(password, user.hashed_password):
        return None
        
    user.last_login = datetime.utcnow()
    db.commit()
    return user

async def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: Session = Depends(get_db)
) -> UserOLM:
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing Authorization header",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    token = credentials.credentials
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, Config.SECRET_KEY, algorithms=[Config.ALGORITHM])
        olm_id: str = payload.get("sub")
        if olm_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
        
    user = db.query(UserOLM).filter(
        UserOLM.olm_id == olm_id,
        UserOLM.is_active == True
    ).first()
    
    if user is None:
        raise credentials_exception
    return user

def require_role(allowed_roles: List[str]):
    def role_checker(current_user: UserOLM = Depends(get_current_user)) -> UserOLM:
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Action requires one of the following roles: {allowed_roles}"
            )
        return current_user
    return role_checker

def seed_initial_users(db: Session):
    # Ensure column exists for backwards-compatibility
    try:
        db.execute(text("ALTER TABLE user_olm ADD COLUMN IF NOT EXISTS hashed_password VARCHAR;"))
        db.commit()
    except Exception:
        db.rollback()

    users = [
        {"olm_id": "OLM_ADMIN_001", "role": "admin"},
        {"olm_id": "OLM_SUPPORT_001", "role": "viewer"},
        {"olm_id": "OLM_SUPPORT_002", "role": "viewer"},
        {"olm_id": "OLM_TECH_001", "role": "tech"},
    ]
    
    default_hash = get_password_hash(DEFAULT_INITIAL_PASSWORD)
    
    for user_data in users:
        existing = db.query(UserOLM).filter(UserOLM.olm_id == user_data["olm_id"]).first()
        if not existing:
            user = UserOLM(
                olm_id=user_data["olm_id"],
                role=user_data["role"],
                hashed_password=default_hash,
                is_active=True
            )
            db.add(user)
        elif not existing.hashed_password:
            existing.hashed_password = default_hash
            db.add(existing)
            
    db.commit()
