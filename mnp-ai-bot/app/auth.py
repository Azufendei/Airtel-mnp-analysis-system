from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from app.models import UserOLM
from app.config import Config

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_olm_id(db: Session, olm_id: str) -> bool:
    user = db.query(UserOLM).filter(
        UserOLM.olm_id == olm_id,
        UserOLM.is_active == True
    ).first()
    
    if user:
        user.last_login = datetime.utcnow()
        db.commit()
        return True
    return False

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, Config.SECRET_KEY, algorithm=Config.ALGORITHM)
    return encoded_jwt

def seed_initial_users(db: Session):
    users = [
        {"olm_id": "OLM_ADMIN_001", "role": "admin"},
        {"olm_id": "OLM_SUPPORT_001", "role": "viewer"},
        {"olm_id": "OLM_SUPPORT_002", "role": "viewer"},
        {"olm_id": "OLM_TECH_001", "role": "tech"},
    ]
    
    for user_data in users:
        existing = db.query(UserOLM).filter(UserOLM.olm_id == user_data["olm_id"]).first()
        if not existing:
            user = UserOLM(**user_data)
            db.add(user)
    db.commit()