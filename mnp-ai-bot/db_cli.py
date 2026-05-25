#!/usr/bin/env python3
"""
Local Database Management CLI Tool

Use this script to manage the database locally without exposing API endpoints.
Restricted to local file-based usage only.

Usage:
    python db_cli.py query <table> [--msisdn MSISDN] [--limit LIMIT]
    python db_cli.py add journey <data.json>
    python db_cli.py add log <data.json>
    python db_cli.py update journey <record_id> <data.json>
    python db_cli.py update log <record_id> <data.json>
    python db_cli.py delete journey <record_id>
    python db_cli.py delete log <record_id>
    python db_cli.py delete-msisdn <table> <msisdn>
    python db_cli.py stats
    python db_cli.py structure <table>
"""

import sys
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional

# Add app to path
sys.path.insert(0, str(Path(__file__).parent))

from sqlalchemy.orm import Session
from app.database import get_db, engine
from app.db_manager import DatabaseManager
from app.models import UserOLM, MNPJourney, ApplicationLog


class LocalDatabaseCLI:
    """Local CLI tool for database management."""
    
    def __init__(self):
        self.db = next(get_db())
        self.manager = DatabaseManager(self.db)
        self.log_file = Path("db_operations.log")
    
    def log_operation(self, operation: str, details: Dict[str, Any]):
        """Log operation to local file."""
        try:
            log_entry = {
                "timestamp": datetime.now().isoformat(),
                "operation": operation,
                "details": details
            }
            
            with open(self.log_file, "a") as f:
                f.write(json.dumps(log_entry) + "\n")
        except Exception as e:
            print(f"⚠️  Warning: Could not log operation: {e}")
    
    def query_table(self, table_name: str, msisdn: Optional[str] = None, limit: int = 100):
        """Query table and save results to local file."""
        try:
            filters = {}
            if msisdn:
                filters["msisdn"] = msisdn
            
            result = self.manager.query_table(table_name, filters, limit)
            
            # Save to local file
            output_file = Path(f"query_{table_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
            with open(output_file, "w") as f:
                json.dump(result, f, indent=2, default=str)
            
            # Print summary
            print(f"\n✅ Query Results:")
            print(f"   Table: {result['table']}")
            print(f"   Records: {result['total_records']}")
            print(f"   Output: {output_file}")
            
            self.log_operation("query", {
                "table": table_name,
                "msisdn": msisdn,
                "records_found": result['total_records'],
                "output_file": str(output_file)
            })
            
            return result
        except Exception as e:
            print(f"❌ Error querying table: {e}")
            return None
    
    def add_journey(self, data_file: str):
        """Add journey record from JSON file."""
        try:
            with open(data_file, "r") as f:
                data = json.load(f)
            
            result = self.manager.add_mnp_journey(data)
            
            print(f"\n✅ Journey Record Added:")
            print(f"   ID: {result['id']}")
            print(f"   MSISDN: {data.get('msisdn')}")
            print(f"   Event: {data.get('event_type')}")
            
            self.log_operation("add_journey", {
                "record_id": result['id'],
                "msisdn": data.get('msisdn'),
                "event_type": data.get('event_type')
            })
            
            return result
        except FileNotFoundError:
            print(f"❌ File not found: {data_file}")
            return None
        except Exception as e:
            print(f"❌ Error adding journey: {e}")
            return None
    
    def add_log(self, data_file: str):
        """Add log record from JSON file."""
        try:
            with open(data_file, "r") as f:
                data = json.load(f)
            
            result = self.manager.add_application_log(data)
            
            print(f"\n✅ Log Record Added:")
            print(f"   ID: {result['id']}")
            print(f"   MSISDN: {data.get('msisdn')}")
            print(f"   Level: {data.get('log_level')}")
            
            self.log_operation("add_log", {
                "record_id": result['id'],
                "msisdn": data.get('msisdn'),
                "log_level": data.get('log_level')
            })
            
            return result
        except FileNotFoundError:
            print(f"❌ File not found: {data_file}")
            return None
        except Exception as e:
            print(f"❌ Error adding log: {e}")
            return None
    
    def update_journey(self, record_id: int, data_file: str):
        """Update journey record from JSON file."""
        try:
            with open(data_file, "r") as f:
                data = json.load(f)
            
            result = self.manager.update_mnp_journey(record_id, data)
            
            print(f"\n✅ Journey Record Updated:")
            print(f"   ID: {record_id}")
            print(f"   MSISDN: {result['data'].get('msisdn')}")
            
            self.log_operation("update_journey", {
                "record_id": record_id,
                "updated_fields": list(data.keys())
            })
            
            return result
        except FileNotFoundError:
            print(f"❌ File not found: {data_file}")
            return None
        except Exception as e:
            print(f"❌ Error updating journey: {e}")
            return None
    
    def update_log(self, record_id: int, data_file: str):
        """Update log record from JSON file."""
        try:
            with open(data_file, "r") as f:
                data = json.load(f)
            
            result = self.manager.update_application_log(record_id, data)
            
            print(f"\n✅ Log Record Updated:")
            print(f"   ID: {record_id}")
            
            self.log_operation("update_log", {
                "record_id": record_id,
                "updated_fields": list(data.keys())
            })
            
            return result
        except FileNotFoundError:
            print(f"❌ File not found: {data_file}")
            return None
        except Exception as e:
            print(f"❌ Error updating log: {e}")
            return None
    
    def delete_journey(self, record_id: int):
        """Delete journey record."""
        try:
            # Confirm operation
            confirm = input(f"⚠️  Delete journey record {record_id}? (yes/no): ")
            if confirm.lower() != "yes":
                print("❌ Operation cancelled")
                return None
            
            result = self.manager.delete_mnp_journey(record_id)
            
            print(f"\n✅ Journey Record Deleted:")
            print(f"   ID: {record_id}")
            print(f"   MSISDN: {result['msisdn']}")
            
            self.log_operation("delete_journey", {
                "record_id": record_id,
                "msisdn": result['msisdn']
            })
            
            return result
        except Exception as e:
            print(f"❌ Error deleting journey: {e}")
            return None
    
    def delete_log(self, record_id: int):
        """Delete log record."""
        try:
            confirm = input(f"⚠️  Delete log record {record_id}? (yes/no): ")
            if confirm.lower() != "yes":
                print("❌ Operation cancelled")
                return None
            
            result = self.manager.delete_application_log(record_id)
            
            print(f"\n✅ Log Record Deleted:")
            print(f"   ID: {record_id}")
            
            self.log_operation("delete_log", {
                "record_id": record_id
            })
            
            return result
        except Exception as e:
            print(f"❌ Error deleting log: {e}")
            return None
    
    def delete_by_msisdn(self, table_name: str, msisdn: str):
        """Delete all records for MSISDN."""
        try:
            # Double confirm for safety
            print(f"⚠️  WARNING: This will delete ALL records for MSISDN {msisdn} from {table_name}")
            confirm1 = input("Type MSISDN to confirm: ")
            if confirm1 != msisdn:
                print("❌ Confirmation failed")
                return None
            
            confirm2 = input("Type 'DELETE' to proceed: ")
            if confirm2 != "DELETE":
                print("❌ Operation cancelled")
                return None
            
            result = self.manager.delete_by_msisdn(table_name, msisdn)
            
            print(f"\n✅ Records Deleted:")
            print(f"   Table: {table_name}")
            print(f"   MSISDN: {msisdn}")
            print(f"   Count: {result['deleted_count']}")
            
            self.log_operation("delete_by_msisdn", {
                "table": table_name,
                "msisdn": msisdn,
                "deleted_count": result['deleted_count']
            })
            
            return result
        except Exception as e:
            print(f"❌ Error deleting by MSISDN: {e}")
            return None
    
    def get_stats(self):
        """Get database statistics."""
        try:
            stats = self.manager.get_database_statistics()
            
            print(f"\n📊 Database Statistics:")
            print(f"   Users: {stats['user_olm_count']}")
            print(f"   Journey Records: {stats['mnp_journey_count']}")
            print(f"   Log Records: {stats['application_log_count']}")
            print(f"   Unique MSISDNs (Journey): {stats['unique_msisdns_in_journey']}")
            print(f"   Unique MSISDNs (Logs): {stats['unique_msisdns_in_logs']}")
            
            # Save to file
            output_file = Path(f"db_stats_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
            with open(output_file, "w") as f:
                json.dump(stats, f, indent=2)
            
            print(f"   Saved to: {output_file}")
            
            self.log_operation("get_stats", stats)
            
            return stats
        except Exception as e:
            print(f"❌ Error getting stats: {e}")
            return None
    
    def get_structure(self, table_name: str):
        """Get table structure."""
        try:
            structure = self.manager.get_table_structure(table_name)
            
            print(f"\n📋 Table Structure: {table_name}")
            print(f"   Columns: {structure['total_columns']}")
            for col in structure['columns']:
                print(f"     - {col['name']}: {col['type']}")
            
            # Save to file
            output_file = Path(f"table_structure_{table_name}.json")
            with open(output_file, "w") as f:
                json.dump(structure, f, indent=2, default=str)
            
            print(f"   Saved to: {output_file}")
            
            return structure
        except Exception as e:
            print(f"❌ Error getting structure: {e}")
            return None
    
    def close(self):
        """Close database session."""
        self.db.close()


def print_help():
    """Print usage help."""
    print(__doc__)


def main():
    """Main CLI entry point."""
    if len(sys.argv) < 2:
        print_help()
        return
    
    command = sys.argv[1].lower()
    cli = LocalDatabaseCLI()
    
    try:
        if command == "help":
            print_help()
        
        elif command == "query" and len(sys.argv) >= 3:
            table = sys.argv[2]
            msisdn = None
            limit = 100
            
            if "--msisdn" in sys.argv:
                idx = sys.argv.index("--msisdn")
                if idx + 1 < len(sys.argv):
                    msisdn = sys.argv[idx + 1]
            
            if "--limit" in sys.argv:
                idx = sys.argv.index("--limit")
                if idx + 1 < len(sys.argv):
                    limit = int(sys.argv[idx + 1])
            
            cli.query_table(table, msisdn, limit)
        
        elif command == "add" and len(sys.argv) >= 4:
            add_type = sys.argv[2].lower()
            data_file = sys.argv[3]
            
            if add_type == "journey":
                cli.add_journey(data_file)
            elif add_type == "log":
                cli.add_log(data_file)
            else:
                print(f"❌ Unknown add type: {add_type}")
        
        elif command == "update" and len(sys.argv) >= 5:
            update_type = sys.argv[2].lower()
            record_id = int(sys.argv[3])
            data_file = sys.argv[4]
            
            if update_type == "journey":
                cli.update_journey(record_id, data_file)
            elif update_type == "log":
                cli.update_log(record_id, data_file)
            else:
                print(f"❌ Unknown update type: {update_type}")
        
        elif command == "delete" and len(sys.argv) >= 4:
            delete_type = sys.argv[2].lower()
            record_id = int(sys.argv[3])
            
            if delete_type == "journey":
                cli.delete_journey(record_id)
            elif delete_type == "log":
                cli.delete_log(record_id)
            else:
                print(f"❌ Unknown delete type: {delete_type}")
        
        elif command == "delete-msisdn" and len(sys.argv) >= 4:
            table = sys.argv[2]
            msisdn = sys.argv[3]
            cli.delete_by_msisdn(table, msisdn)
        
        elif command == "stats":
            cli.get_stats()
        
        elif command == "structure" and len(sys.argv) >= 3:
            table = sys.argv[2]
            cli.get_structure(table)
        
        else:
            print(f"❌ Unknown command: {command}")
            print_help()
    
    finally:
        cli.close()


if __name__ == "__main__":
    main()
