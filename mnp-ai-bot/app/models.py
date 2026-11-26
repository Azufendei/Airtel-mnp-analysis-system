from sqlalchemy import Column, Integer, String, DateTime, Boolean, JSON, Text, Index
from sqlalchemy.sql import func
from app.database import Base

class UserOLM(Base):
    __tablename__ = "user_olm"
    
    id = Column(Integer, primary_key=True, index=True)
    olm_id = Column(String, unique=True, index=True, nullable=False)
    role = Column(String, default="viewer")
    hashed_password = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_login = Column(DateTime(timezone=True), nullable=True)

class MNPJourney(Base):
    __tablename__ = "mnp_journey"
    
    id = Column(Integer, primary_key=True, index=True)
    msisdn = Column(String, index=True, nullable=False)
    event_type = Column(String, nullable=False)
    timestamp = Column(DateTime(timezone=True), nullable=False, index=True)
    operator = Column(String)
    circle = Column(String)
    result = Column(String)
    txn_id = Column(String, unique=True, index=True)
    details = Column(JSON, default={})
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    __table_args__ = (
        Index('idx_msisdn_timestamp', 'msisdn', 'timestamp'),
    )

class ApplicationLog(Base):
    __tablename__ = "application_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    msisdn = Column(String, index=True)
    log_time = Column(DateTime(timezone=True), nullable=False, index=True)
    log_level = Column(String)
    source = Column(String)
    message = Column(Text)
    extracted = Column(JSON, default={})
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    __table_args__ = (
        Index('idx_logs_msisdn_time', 'msisdn', 'log_time'),
    )
