# Local Database Management - CLI Tool Guide

Complete guide to using the local database management CLI tool.

---

## Overview

The database management operations are restricted to **local file-based usage only**. There are no API endpoints exposed. All database operations use the `db_cli.py` script.

**Benefits:**
- ✅ Secure - no API exposure
- ✅ Local - only developers with database access can modify data
- ✅ Logged - all operations recorded in `db_operations.log`
- ✅ Safe - confirmation prompts for dangerous operations
- ✅ Traceable - output files with timestamps

---

## Quick Start

### Prerequisites
```bash
cd mnp-ai-bot
python -m venv venv
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate
pip install -r requirements.txt
```

### View Help
```bash
python db_cli.py help
```

### Check Database Stats
```bash
python db_cli.py stats
```

---

## Available Commands

### 1. Query Data

**Query all records from a table:**
```bash
python db_cli.py query mnp_journey
```

**Query with MSISDN filter:**
```bash
python db_cli.py query mnp_journey --msisdn 919890123456
```

**Query with limit:**
```bash
python db_cli.py query application_log --limit 50
```

**Query combined:**
```bash
python db_cli.py query mnp_journey --msisdn 919890123456 --limit 10
```

**Output:** Results saved to `query_mnp_journey_YYYYMMDD_HHMMSS.json`

---

### 2. Add Records

**Create journey_data.json:**
```json
{
  "msisdn": "919890123456",
  "event_type": "Port_in",
  "timestamp": "2026-05-26T10:30:00",
  "operator": "Jio",
  "circle": "Mumbai",
  "result": "Success",
  "txn_id": "TXN123456",
  "details": {
    "donor": "Airtel",
    "recipient": "Jio",
    "reason": "Better plans"
  }
}
```

**Add journey record:**
```bash
python db_cli.py add journey journey_data.json
```

**Create log_data.json:**
```json
{
  "msisdn": "919890123456",
  "log_time": "2026-05-26T10:30:00",
  "log_level": "INFO",
  "source": "API",
  "message": "Port-in request received successfully",
  "extracted": {
    "request_type": "port_in",
    "processing_time": "2.5s"
  }
}
```

**Add log record:**
```bash
python db_cli.py add log log_data.json
```

---

### 3. Update Records

**Create update_data.json:**
```json
{
  "result": "Failed",
  "details": {
    "reason": "Donor rejected request",
    "error_code": "DONOR_REJECTION"
  }
}
```

**Update journey record (ID = 5):**
```bash
python db_cli.py update journey 5 update_data.json
```

**Update log record (ID = 5):**
```bash
python db_cli.py update log 5 update_data.json
```

---

### 4. Delete Records

**Delete journey record (ID = 5):**
```bash
python db_cli.py delete journey 5
```

You'll be prompted to confirm:
```
⚠️  Delete journey record 5? (yes/no): yes
```

**Delete log record:**
```bash
python db_cli.py delete log 10
```

**Delete all records for MSISDN (requires double confirmation):**
```bash
python db_cli.py delete-msisdn mnp_journey 919890123456
```

First prompt:
```
⚠️  WARNING: This will delete ALL records for MSISDN 919890123456 from mnp_journey
Type MSISDN to confirm: 919890123456
Type 'DELETE' to proceed: DELETE
```

---

### 5. View Statistics

**Get database statistics:**
```bash
python db_cli.py stats
```

Output:
```
📊 Database Statistics:
   Users: 3
   Journey Records: 15
   Log Records: 42
   Unique MSISDNs (Journey): 5
   Unique MSISDNs (Logs): 6
   Saved to: db_stats_20260526_103000.json
```

---

### 6. View Table Structure

**Get table schema:**
```bash
python db_cli.py structure mnp_journey
```

Output:
```
📋 Table Structure: mnp_journey
   Columns: 10
     - id: INTEGER
     - msisdn: VARCHAR
     - event_type: VARCHAR
     - timestamp: DATETIME
     - operator: VARCHAR
     - circle: VARCHAR
     - result: VARCHAR
     - txn_id: VARCHAR
     - details: JSON
     - created_at: DATETIME
   Saved to: table_structure_mnp_journey.json
```

---

## Real-World Workflows

### Workflow 1: Track a Customer Journey

```bash
# 1. Check if data exists
python db_cli.py query mnp_journey --msisdn 919890123456

# 2. Create journey_event1.json
# (see example above)

# 3. Add first event
python db_cli.py add journey journey_event1.json

# 4. Create and add follow-up event
# Create journey_event2.json with new event_type (e.g., NPD_IN)
python db_cli.py add journey journey_event2.json

# 5. View complete timeline
python db_cli.py query mnp_journey --msisdn 919890123456
```

### Workflow 2: Debug Issues with Logs

```bash
# 1. Get recent logs
python db_cli.py query application_log --limit 50

# 2. Find logs for specific number
python db_cli.py query application_log --msisdn 919890123456

# 3. From results, find error records and their IDs

# 4. Update error log with more diagnostic info
# Create diagnostic_update.json
python db_cli.py update log <ID> diagnostic_update.json

# 5. View updated record
python db_cli.py query application_log --limit 1
```

### Workflow 3: Backup Data

```bash
# 1. Get all journey records
python db_cli.py query mnp_journey --limit 1000

# 2. Backup file created: query_mnp_journey_YYYYMMDD_HHMMSS.json

# 3. Get all logs
python db_cli.py query application_log --limit 1000

# 4. Get statistics
python db_cli.py stats

# Now you have all data backed up locally
```

### Workflow 4: Cleanup Old Data

```bash
# 1. Check statistics before cleanup
python db_cli.py stats

# 2. Query records for specific MSISDN
python db_cli.py query mnp_journey --msisdn 9198888888888

# 3. If it's test/temporary data, delete it
python db_cli.py delete-msisdn mnp_journey 9198888888888

# 4. Verify cleanup
python db_cli.py stats
```

---

## Example JSON Files

### Journey Record - Port In
```json
{
  "msisdn": "919890123456",
  "event_type": "Port_in",
  "timestamp": "2026-05-26T08:00:00",
  "operator": "Jio",
  "circle": "Mumbai",
  "result": "Success",
  "txn_id": "TXN001",
  "details": {
    "donor": "Airtel",
    "recipient": "Jio",
    "port_in_code": "PI123456"
  }
}
```

### Journey Record - Port Out
```json
{
  "msisdn": "919876543210",
  "event_type": "Port_out",
  "timestamp": "2026-05-26T09:00:00",
  "operator": "Airtel",
  "circle": "Delhi",
  "result": "Success",
  "txn_id": "TXN002",
  "details": {
    "recipient": "Vodafone",
    "port_out_code": "PO789012"
  }
}
```

### Journey Record - Failed
```json
{
  "msisdn": "919890123456",
  "event_type": "Number_return",
  "timestamp": "2026-05-26T10:00:00",
  "operator": "Jio",
  "circle": "Mumbai",
  "result": "Failed",
  "txn_id": "TXN003",
  "details": {
    "reason": "Cooling period violation",
    "error_code": "COOL_PERIOD_VIOLATION",
    "days_since_port_in": 5
  }
}
```

### Log Record - Info
```json
{
  "msisdn": "919890123456",
  "log_time": "2026-05-26T08:00:00",
  "log_level": "INFO",
  "source": "API",
  "message": "Port-in request received successfully",
  "extracted": {
    "endpoint": "/port-in",
    "request_size_bytes": 512,
    "processing_time_ms": 120
  }
}
```

### Log Record - Error
```json
{
  "msisdn": "919890123456",
  "log_time": "2026-05-26T10:30:00",
  "log_level": "ERROR",
  "source": "Orchestrator",
  "message": "Port-in failed: Donor operator rejected request",
  "extracted": {
    "component": "donor_validator",
    "error_type": "REJECTION",
    "rejection_reason": "INVALID_CREDENTIALS",
    "retry_attempt": 2
  }
}
```

### Update Record - Result Change
```json
{
  "result": "Failed",
  "details": {
    "reason": "Donor validation failed",
    "error_code": "DONOR_VALIDATION_FAILED",
    "timestamp_of_failure": "2026-05-26T09:45:00"
  }
}
```

---

## Operation Log File

All operations are logged to `db_operations.log` (JSON lines format).

**View logs:**
```bash
# Show all operations
cat db_operations.log

# Pretty print (Linux/macOS)
cat db_operations.log | jq '.'

# Filter by operation type
grep "query" db_operations.log | jq '.operation'

# Filter by MSISDN
grep "919890123456" db_operations.log
```

**Log entry example:**
```json
{
  "timestamp": "2026-05-26T10:30:00.123456",
  "operation": "add_journey",
  "details": {
    "record_id": 42,
    "msisdn": "919890123456",
    "event_type": "Port_in"
  }
}
```

---

## Query Results Files

Query results are automatically saved to JSON files with timestamps.

**File naming:** `query_<table>_<YYYYMMDD_HHMMSS>.json`

**Example:** `query_mnp_journey_20260526_103000.json`

**Structure:**
```json
{
  "table": "mnp_journey",
  "total_records": 3,
  "limit": 100,
  "data": [
    {
      "id": 1,
      "msisdn": "919890123456",
      "event_type": "Port_in",
      "timestamp": "2026-05-26T10:30:00",
      ...
    }
  ]
}
```

---

## Field Reference

### MNP Journey - Required Fields
| Field | Type | Format | Example |
|-------|------|--------|---------|
| msisdn | string | 10-15 digits | "919890123456" |
| event_type | string | MNP event | "Port_in" |
| timestamp | string | ISO 8601 | "2026-05-26T10:30:00" |
| operator | string | Operator name | "Jio" |
| circle | string | Service circle | "Mumbai" |
| result | string | Success/Failed | "Success" |
| txn_id | string | Transaction ID | "TXN123456" |
| details | object | JSON metadata | {...} |

### Application Log - Required Fields
| Field | Type | Format | Example |
|-------|------|--------|---------|
| msisdn | string | 10-15 digits | "919890123456" |
| log_time | string | ISO 8601 | "2026-05-26T10:30:00" |
| log_level | string | Log level | "INFO" |
| source | string | Log source | "API" |
| message | string | Log message | "Request received" |
| extracted | object | JSON data | {...} |

**Valid Log Levels:** INFO, WARNING, ERROR, DEBUG, CRITICAL

**Valid Event Types:** Port_in, Port_out, NPD_IN, NPD_OUT, Number_return, etc.

---

## Safety Features

### Confirmation Prompts
- ✅ Single delete (record): Requires "yes"
- ✅ Bulk delete (by MSISDN): Requires typing MSISDN + typing "DELETE"

### Operation Logging
- ✅ All operations logged to `db_operations.log`
- ✅ Timestamps on all entries
- ✅ Audit trail for compliance

### Output Files
- ✅ Query results auto-saved with timestamp
- ✅ Stats saved with timestamp
- ✅ Structure saved with table name
- ✅ No data lost, always have backup

---

## Troubleshooting

### Error: "File not found"
- Check file path is correct
- Use absolute path if relative path doesn't work
- Verify JSON file is in current directory or use full path

### Error: "Invalid JSON"
- Validate JSON format at jsonlint.com
- Check for missing commas
- Ensure all quotes are closed
- No trailing commas allowed

### Error: "Missing required field"
- Check field names are spelled correctly
- Ensure all required fields are present
- Verify field values are proper types (string, object, etc.)

### Error: "Record not found"
- Verify record ID exists
- Query table first to find correct ID
- Check if record was already deleted

### Database Connection Error
- Ensure PostgreSQL is running
- Check DATABASE_URL in .env file
- Verify database credentials
- Ensure database exists and user has access

---

## Best Practices

### Do's ✅
- ✅ Always query first to verify data exists
- ✅ Use ISO 8601 format for timestamps
- ✅ Keep JSON files for reference
- ✅ Back up before bulk operations
- ✅ Review logs regularly
- ✅ Use descriptive operation details
- ✅ Check operation results before proceeding

### Don'ts ❌
- ❌ Don't skip confirmation prompts
- ❌ Don't modify ID fields manually
- ❌ Don't use invalid timestamp format
- ❌ Don't delete production data without backup
- ❌ Don't ignore operation logs
- ❌ Don't edit query result files before archiving
- ❌ Don't commit db_operations.log to git

---

## Example Commands Cheat Sheet

```bash
# View stats
python db_cli.py stats

# Query without filter (all records, limit 100)
python db_cli.py query mnp_journey

# Query with MSISDN filter
python db_cli.py query mnp_journey --msisdn 919890123456

# Query with limit
python db_cli.py query application_log --limit 50

# Add journey
python db_cli.py add journey journey_data.json

# Add log
python db_cli.py add log log_data.json

# Update journey
python db_cli.py update journey 5 update_data.json

# Delete journey
python db_cli.py delete journey 5

# Delete all for MSISDN (careful!)
python db_cli.py delete-msisdn mnp_journey 919890123456

# View table structure
python db_cli.py structure mnp_journey
```

---

## Automation Notes

The CLI tool can be integrated into automation scripts:

```bash
#!/bin/bash

# Backup daily
python db_cli.py query mnp_journey --limit 10000 > /backup/journey_$(date +%Y%m%d).json
python db_cli.py query application_log --limit 10000 > /backup/logs_$(date +%Y%m%d).json

# Get stats
python db_cli.py stats
```

---

## Security

- ✅ Local access only (no API exposure)
- ✅ Requires database credentials in .env
- ✅ Confirmation prompts for destructive ops
- ✅ All operations logged with timestamps
- ✅ No data transmission over network
- ✅ File-based output (can be encrypted/archived)

---

**Version**: 1.0  
**Status**: Production Ready  
**Last Updated**: 2026-05-26
