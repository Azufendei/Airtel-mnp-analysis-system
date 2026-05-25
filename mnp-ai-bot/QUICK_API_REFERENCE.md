# Quick API Reference - Database Management

**Base URL**: `http://localhost:8000`  
**Authentication**: Add `?olm_id=USER001` to all requests

---

## Query Operations

```bash
# Get all tables
curl "http://localhost:8000/db/tables?olm_id=USER001"

# Get table structure
curl "http://localhost:8000/db/structure/mnp_journey?olm_id=USER001"

# Database stats
curl "http://localhost:8000/db/stats?olm_id=USER001"

# Count records
curl "http://localhost:8000/db/count/mnp_journey?olm_id=USER001"

# Query with filters
curl "http://localhost:8000/db/query/mnp_journey?olm_id=USER001&msisdn=919890123456&limit=50"
```

---

## Add Operations

```bash
# Add journey record
curl -X POST "http://localhost:8000/db/add/journey?olm_id=USER001" \
  -H "Content-Type: application/json" \
  -d '{
    "msisdn": "919890123456",
    "event_type": "Port_in",
    "timestamp": "2026-05-25T10:30:00",
    "operator": "Jio",
    "circle": "Mumbai",
    "result": "Success",
    "txn_id": "TXN123456",
    "details": {"donor": "Airtel"}
  }'

# Add log record
curl -X POST "http://localhost:8000/db/add/log?olm_id=USER001" \
  -H "Content-Type: application/json" \
  -d '{
    "msisdn": "919890123456",
    "log_time": "2026-05-25T10:30:00",
    "log_level": "ERROR",
    "source": "API",
    "message": "Port-in failed"
  }'

# Add user (admin only)
curl -X POST "http://localhost:8000/db/add/user?olm_id=USER001&new_olm_id=USER004&role=user"
```

---

## Update Operations

```bash
# Update journey (ID = 1)
curl -X PUT "http://localhost:8000/db/update/journey/1?olm_id=USER001" \
  -H "Content-Type: application/json" \
  -d '{"result": "Failed", "details": {"reason": "Updated"}}'

# Update log (ID = 1)
curl -X PUT "http://localhost:8000/db/update/log/1?olm_id=USER001" \
  -H "Content-Type: application/json" \
  -d '{"log_level": "WARNING"}'
```

---

## Delete Operations

```bash
# Delete journey record (ID = 1)
curl -X DELETE "http://localhost:8000/db/delete/journey/1?olm_id=USER001"

# Delete log record (ID = 1)
curl -X DELETE "http://localhost:8000/db/delete/log/1?olm_id=USER001"

# Delete all records for MSISDN (admin only)
curl -X DELETE "http://localhost:8000/db/delete/by-msisdn/mnp_journey/919890123456?olm_id=USER001"
```

---

## Default OLM IDs

| ID     | Role  | Notes |
|--------|-------|-------|
| USER001 | admin | Full access including admin operations |
| USER002 | user  | Standard user access |
| USER003 | user  | Standard user access |

---

## Field References

### MNP Journey Fields
- `msisdn` (required): Phone number
- `event_type` (required): Port_in, Port_out, NPD_IN, etc.
- `timestamp` (required): ISO 8601 format
- `operator` (required): Operator name
- `circle` (required): Service circle
- `result` (required): Success/Failed
- `txn_id` (required): Transaction ID
- `details` (optional): JSON object

### Application Log Fields
- `msisdn` (required): Phone number
- `log_time` (required): ISO 8601 format
- `log_level` (required): INFO, WARNING, ERROR, etc.
- `source` (required): API, Orchestrator, etc.
- `message` (required): Log message text
- `extracted` (optional): JSON object

---

## Common Workflows

### View All Data for an MSISDN
```bash
MSISDN="919890123456"
olm_id="USER001"

# Query journey
curl "http://localhost:8000/db/query/mnp_journey?olm_id=$olm_id&msisdn=$MSISDN"

# Query logs
curl "http://localhost:8000/db/query/application_log?olm_id=$olm_id&msisdn=$MSISDN"
```

### Add and Verify Record
```bash
# Add record
curl -X POST "http://localhost:8000/db/add/journey?olm_id=USER001" \
  -H "Content-Type: application/json" \
  -d '...' > response.json

# Extract ID from response and query
RECORD_ID=$(jq -r '.id' response.json)

# Verify by querying
curl "http://localhost:8000/db/query/mnp_journey?olm_id=USER001&limit=1"
```

### Update and Delete
```bash
# Get record ID from query
RECORD_ID=1

# Update
curl -X PUT "http://localhost:8000/db/update/journey/$RECORD_ID?olm_id=USER001" \
  -H "Content-Type: application/json" \
  -d '{"result": "Updated"}'

# Delete
curl -X DELETE "http://localhost:8000/db/delete/journey/$RECORD_ID?olm_id=USER001"
```

---

## Response Examples

### Success
```json
{
  "status": "success",
  "message": "Record added",
  "id": 42,
  "data": {...}
}
```

### Error
```json
{
  "detail": "Invalid OLM ID"
}
```

### Query
```json
{
  "table": "mnp_journey",
  "total_records": 3,
  "limit": 100,
  "data": [...]
}
```

---

## Interactive Testing

1. Start backend: `uvicorn app.main:app --reload`
2. Open: `http://localhost:8000/docs`
3. All endpoints available with "Try it out" buttons
4. Real-time API testing and schema validation

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| 401 Invalid OLM ID | Check olm_id parameter and ensure user is active |
| 403 Forbidden | Operation requires admin role |
| 400 Bad Request | Check JSON format and required fields |
| 500 Server Error | Check database connection and server logs |

---

**See DATABASE_MANAGEMENT_API.md for complete endpoint documentation.**
