"""
Database Management Module

Provides CRUD operations for the MNP database.
Allows querying, viewing, adding, updating, and deleting records.

Protected by OLM ID authentication - only admin users can perform these operations.
"""

from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from sqlalchemy import inspect, text
import json
from datetime import datetime

from app.models import MNPJourney, ApplicationLog, UserOLM
from app.auth import verify_olm_id


class DatabaseManager:
    """Manages database operations with proper access control and error handling."""
    
    def __init__(self, db: Session):
        self.db = db
    
    # ================================================================
    #  TABLE OPERATIONS
    # ================================================================
    
    def get_tables(self) -> List[str]:
        """Get list of all tables in the database."""
        try:
            inspector = inspect(self.db.get_bind())
            return inspector.get_table_names()
        except Exception as e:
            raise Exception(f"Failed to get tables: {str(e)}")
    
    def get_table_structure(self, table_name: str) -> Dict[str, Any]:
        """Get structure and column info for a table."""
        try:
            inspector = inspect(self.db.get_bind())
            
            if table_name not in inspector.get_table_names():
                raise ValueError(f"Table '{table_name}' does not exist")
            
            columns = inspector.get_columns(table_name)
            primary_keys = inspector.get_pk_constraint(table_name)
            
            return {
                "table_name": table_name,
                "columns": columns,
                "primary_keys": primary_keys.get("constrained_columns", []),
                "total_columns": len(columns)
            }
        except Exception as e:
            raise Exception(f"Failed to get table structure: {str(e)}")
    
    # ================================================================
    #  QUERY OPERATIONS
    # ================================================================
    
    def query_table(self, table_name: str, filters: Dict[str, Any] = None, limit: int = 100) -> Dict[str, Any]:
        """Query a table with optional filters."""
        try:
            # Map table names to models
            model_map = {
                "user_olm": UserOLM,
                "mnp_journey": MNPJourney,
                "application_log": ApplicationLog
            }
            
            if table_name not in model_map:
                raise ValueError(f"Table '{table_name}' is not accessible")
            
            model = model_map[table_name]
            query = self.db.query(model)
            
            # Apply filters if provided
            if filters:
                for key, value in filters.items():
                    if hasattr(model, key):
                        query = query.filter(getattr(model, key) == value)
            
            # Apply limit
            query = query.limit(limit)
            
            # Execute and convert to dict
            records = query.all()
            total_records = len(records)
            
            # Convert to dictionary
            data = []
            for record in records:
                record_dict = {}
                for column in inspect(model).columns:
                    value = getattr(record, column.name)
                    # Handle datetime serialization
                    if isinstance(value, datetime):
                        record_dict[column.name] = value.isoformat()
                    # Handle JSON fields
                    elif isinstance(value, dict):
                        record_dict[column.name] = value
                    else:
                        record_dict[column.name] = value
                data.append(record_dict)
            
            return {
                "table": table_name,
                "total_records": total_records,
                "limit": limit,
                "data": data
            }
        except Exception as e:
            raise Exception(f"Query failed: {str(e)}")
    
    def get_record_count(self, table_name: str) -> Dict[str, Any]:
        """Get total record count for a table."""
        try:
            model_map = {
                "user_olm": UserOLM,
                "mnp_journey": MNPJourney,
                "application_log": ApplicationLog
            }
            
            if table_name not in model_map:
                raise ValueError(f"Table '{table_name}' is not accessible")
            
            model = model_map[table_name]
            count = self.db.query(model).count()
            
            return {
                "table": table_name,
                "total_records": count
            }
        except Exception as e:
            raise Exception(f"Failed to count records: {str(e)}")
    
    # ================================================================
    #  ADD/INSERT OPERATIONS
    # ================================================================
    
    def add_mnp_journey(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Add a new MNP journey record."""
        try:
            # Validate required fields
            required_fields = ["msisdn", "event_type", "timestamp", "operator", "circle", "result", "txn_id"]
            for field in required_fields:
                if field not in data:
                    raise ValueError(f"Missing required field: {field}")
            
            # Create new record
            record = MNPJourney(
                msisdn=data["msisdn"],
                event_type=data["event_type"],
                timestamp=data["timestamp"] if isinstance(data["timestamp"], datetime) else datetime.fromisoformat(data["timestamp"]),
                operator=data.get("operator"),
                circle=data.get("circle"),
                result=data.get("result"),
                txn_id=data.get("txn_id"),
                details=data.get("details", {})
            )
            
            self.db.add(record)
            self.db.commit()
            self.db.refresh(record)
            
            return {
                "status": "success",
                "message": "MNP journey record added",
                "id": record.id,
                "data": {
                    "msisdn": record.msisdn,
                    "event_type": record.event_type,
                    "timestamp": record.timestamp.isoformat(),
                    "txn_id": record.txn_id
                }
            }
        except Exception as e:
            self.db.rollback()
            raise Exception(f"Failed to add MNP journey: {str(e)}")
    
    def add_application_log(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Add a new application log record."""
        try:
            # Validate required fields
            required_fields = ["msisdn", "log_time", "log_level", "source", "message"]
            for field in required_fields:
                if field not in data:
                    raise ValueError(f"Missing required field: {field}")
            
            # Create new record
            record = ApplicationLog(
                msisdn=data["msisdn"],
                log_time=data["log_time"] if isinstance(data["log_time"], datetime) else datetime.fromisoformat(data["log_time"]),
                log_level=data["log_level"],
                source=data["source"],
                message=data["message"],
                extracted=data.get("extracted", {})
            )
            
            self.db.add(record)
            self.db.commit()
            self.db.refresh(record)
            
            return {
                "status": "success",
                "message": "Application log record added",
                "id": record.id,
                "data": {
                    "msisdn": record.msisdn,
                    "log_time": record.log_time.isoformat(),
                    "log_level": record.log_level,
                    "source": record.source
                }
            }
        except Exception as e:
            self.db.rollback()
            raise Exception(f"Failed to add application log: {str(e)}")
    
    def add_user(self, olm_id: str, role: str = "user", is_active: bool = True) -> Dict[str, Any]:
        """Add a new user/OLM ID."""
        try:
            # Check if user already exists
            existing = self.db.query(UserOLM).filter(UserOLM.olm_id == olm_id).first()
            if existing:
                raise ValueError(f"OLM ID '{olm_id}' already exists")
            
            # Create new user
            user = UserOLM(
                olm_id=olm_id,
                role=role,
                is_active=is_active
            )
            
            self.db.add(user)
            self.db.commit()
            self.db.refresh(user)
            
            return {
                "status": "success",
                "message": "User added",
                "id": user.id,
                "data": {
                    "olm_id": user.olm_id,
                    "role": user.role,
                    "is_active": user.is_active,
                    "created_at": user.created_at.isoformat() if user.created_at else None
                }
            }
        except Exception as e:
            self.db.rollback()
            raise Exception(f"Failed to add user: {str(e)}")
    
    # ================================================================
    #  UPDATE OPERATIONS
    # ================================================================
    
    def update_mnp_journey(self, record_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        """Update an MNP journey record."""
        try:
            record = self.db.query(MNPJourney).filter(MNPJourney.id == record_id).first()
            if not record:
                raise ValueError(f"Record with ID {record_id} not found")
            
            # Update fields
            for key, value in data.items():
                if hasattr(record, key) and key != "id":
                    if key in ["timestamp"]:
                        value = value if isinstance(value, datetime) else datetime.fromisoformat(value)
                    setattr(record, key, value)
            
            self.db.commit()
            self.db.refresh(record)
            
            return {
                "status": "success",
                "message": f"Record {record_id} updated",
                "id": record.id,
                "data": {
                    "msisdn": record.msisdn,
                    "event_type": record.event_type,
                    "timestamp": record.timestamp.isoformat()
                }
            }
        except Exception as e:
            self.db.rollback()
            raise Exception(f"Failed to update record: {str(e)}")
    
    def update_application_log(self, record_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        """Update an application log record."""
        try:
            record = self.db.query(ApplicationLog).filter(ApplicationLog.id == record_id).first()
            if not record:
                raise ValueError(f"Record with ID {record_id} not found")
            
            # Update fields
            for key, value in data.items():
                if hasattr(record, key) and key != "id":
                    if key in ["log_time"]:
                        value = value if isinstance(value, datetime) else datetime.fromisoformat(value)
                    setattr(record, key, value)
            
            self.db.commit()
            self.db.refresh(record)
            
            return {
                "status": "success",
                "message": f"Record {record_id} updated",
                "id": record.id
            }
        except Exception as e:
            self.db.rollback()
            raise Exception(f"Failed to update record: {str(e)}")
    
    # ================================================================
    #  DELETE OPERATIONS
    # ================================================================
    
    def delete_mnp_journey(self, record_id: int) -> Dict[str, Any]:
        """Delete an MNP journey record."""
        try:
            record = self.db.query(MNPJourney).filter(MNPJourney.id == record_id).first()
            if not record:
                raise ValueError(f"Record with ID {record_id} not found")
            
            msisdn = record.msisdn
            self.db.delete(record)
            self.db.commit()
            
            return {
                "status": "success",
                "message": f"Record {record_id} deleted",
                "deleted_id": record_id,
                "msisdn": msisdn
            }
        except Exception as e:
            self.db.rollback()
            raise Exception(f"Failed to delete record: {str(e)}")
    
    def delete_application_log(self, record_id: int) -> Dict[str, Any]:
        """Delete an application log record."""
        try:
            record = self.db.query(ApplicationLog).filter(ApplicationLog.id == record_id).first()
            if not record:
                raise ValueError(f"Record with ID {record_id} not found")
            
            msisdn = record.msisdn
            self.db.delete(record)
            self.db.commit()
            
            return {
                "status": "success",
                "message": f"Record {record_id} deleted",
                "deleted_id": record_id,
                "msisdn": msisdn
            }
        except Exception as e:
            self.db.rollback()
            raise Exception(f"Failed to delete record: {str(e)}")
    
    def delete_by_msisdn(self, table_name: str, msisdn: str) -> Dict[str, Any]:
        """Delete all records for a specific MSISDN."""
        try:
            model_map = {
                "mnp_journey": MNPJourney,
                "application_log": ApplicationLog
            }
            
            if table_name not in model_map:
                raise ValueError(f"Cannot delete from table '{table_name}'")
            
            model = model_map[table_name]
            deleted_count = self.db.query(model).filter(model.msisdn == msisdn).delete()
            self.db.commit()
            
            return {
                "status": "success",
                "message": f"Deleted {deleted_count} records for MSISDN {msisdn}",
                "table": table_name,
                "msisdn": msisdn,
                "deleted_count": deleted_count
            }
        except Exception as e:
            self.db.rollback()
            raise Exception(f"Failed to delete records: {str(e)}")
    
    # ================================================================
    #  STATISTICS
    # ================================================================
    
    def get_database_statistics(self) -> Dict[str, Any]:
        """Get statistics about the database."""
        try:
            return {
                "user_olm_count": self.db.query(UserOLM).count(),
                "mnp_journey_count": self.db.query(MNPJourney).count(),
                "application_log_count": self.db.query(ApplicationLog).count(),
                "unique_msisdns_in_journey": self.db.query(MNPJourney.msisdn).distinct().count(),
                "unique_msisdns_in_logs": self.db.query(ApplicationLog.msisdn).distinct().count(),
            }
        except Exception as e:
            raise Exception(f"Failed to get statistics: {str(e)}")
