# Quick API Reference - Enterprise MNP Analysis Engine

**Base URL**: `http://localhost:8000`  
**Authentication Standard**: OAuth2 Password Flow with signed JSON Web Tokens (JWT Bearer standard)  
**Header Format**: `Authorization: Bearer <access_token>`

---

## 🔐 Seeded Enterprise Credentials

All accounts are pre-seeded with salted `bcrypt` password hashes by `python setup_db.py`:

| OLM ID | Role | Access Level | Default Password |
|---|---|---|---|
| `OLM_ADMIN_001` | `admin` | Full system access, user management, admin data routes | `Password@123` |
| `OLM_TECH_001` | `tech` | Technical operations, user directory access, analytics | `Password@123` |
| `OLM_SUPPORT_001`| `support` | Subscriber journey lookup, resolution, log audits | `Password@123` |
| `OLM_EXEC_001` | `viewer` | Read-only analytics, dashboard viewer | `Password@123` |

---

## 🔑 Authentication Endpoints

### 1. Authenticate & Obtain JWT Token
```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "olm_id": "OLM_ADMIN_001",
    "password": "Password@123"
  }'
```
**Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "olm_id": "OLM_ADMIN_001",
    "role": "admin",
    "is_active": true,
    "last_login": "2026-11-26T21:00:00.000Z"
  }
}
```

### 2. Verify Session Profile
```bash
TOKEN="<your_jwt_access_token>"

curl -X GET "http://localhost:8000/auth/me" \
  -H "Authorization: Bearer $TOKEN"
```
**Response (200 OK):**
```json
{
  "olm_id": "OLM_ADMIN_001",
  "role": "admin",
  "is_active": true,
  "last_login": "2026-11-26T21:00:00.000Z"
}
```

---

## 📊 Core Analytics Endpoints

### 3. Analyze MNP Subscriber Journey
Analyzes subscriber timeline across gateways, detects TRAI compliance breaches (e.g. 10-day cooling period), and synthesizes AI-powered recommendations.

```bash
curl -X POST "http://localhost:8000/analyze" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "msisdn": "919890123456",
    "start_time": "2026-05-01T00:00:00",
    "end_time": "2026-05-30T23:59:59"
  }'
```

**Response (200 OK):**
```json
{
  "msisdn": "919890123456",
  "time_range": {
    "start": "2026-05-01T00:00:00",
    "end": "2026-05-30T23:59:59"
  },
  "tabular_journey": [
    {
      "event_type": "Port_in",
      "timestamp": "2026-05-24T10:00:00",
      "operator": "Jio",
      "circle": "Mumbai",
      "result": "Success",
      "txn_id": "TXN1716544800",
      "details": {"donor": "Airtel", "recipient": "Jio"}
    },
    {
      "event_type": "Number_return",
      "timestamp": "2026-05-26T10:00:00",
      "operator": "Airtel",
      "circle": "Mumbai",
      "result": "Failed",
      "txn_id": "TXN1716717600",
      "details": {"reason": "Cooling period violation"}
    }
  ],
  "tabular_text": "+------------+---------------------+----------+--------+--------+---------------+\n| Event Type | Timestamp           | Operator | Circle | Result | Txn ID        |\n+------------+---------------------+----------+--------+--------+---------------+\n...",
  "logs_analysis": {
    "summary": "Analyzed 2 log entries. Found 1 errors, 0 warnings, and 1 info messages.",
    "error_count": 1,
    "warning_count": 0,
    "info_count": 1,
    "key_issues": [
      "Critical issue detected: Number return failed: Donor operator rejected due to cooling period violation"
    ],
    "timeline": {
      "2026-05-24": 1,
      "2026-05-26": 1
    }
  },
  "suggestions": [
    {
      "category": "Warnings",
      "priority": "critical",
      "suggestion": "Number return within 2 days of port-in — 10-day cooling period violation",
      "details": "This warning indicates a potential issue with your MNP process."
    },
    {
      "category": "Recommendations",
      "priority": "high",
      "suggestion": "Wait for cooling period to complete before retrying number return",
      "details": "This is a recommended action based on analysis of your MNP journey."
    }
  ],
  "status": "Success"
}
```

---

## 🛡️ Administrative & System Endpoints

### 4. Health & Liveness Probe
```bash
curl -X GET "http://localhost:8000/health"
```
**Response (200 OK):**
```json
{
  "status": "healthy",
  "timestamp": "2026-11-26T21:05:00.000Z",
  "version": "1.1.0",
  "environment": "production"
}
```

### 5. List Registered OLM Users (RBAC: Admin / Tech Only)
```bash
curl -X GET "http://localhost:8000/users" \
  -H "Authorization: Bearer $TOKEN"
```
*Note: Returns `403 Forbidden` if called by `support` or `viewer` accounts.*

### 6. Bootstrap Sample Journey & Gateway Logs
Populates an active MNP journey with a built-in 2-day return cooling period violation for testing:
```bash
curl -X POST "http://localhost:8000/admin/insert_sample_data"
```

---

## 🛠️ Local Database Management CLI

Direct database maintenance, bulk exports, and schema inspection are restricted to the local CLI utility:

```bash
# Display CLI commands
python db_cli.py help

# Database statistics
python db_cli.py stats

# Filtered journey queries
python db_cli.py query mnp_journey --msisdn 919890123456 --limit 50
```
*See [DATABASE_CLI_GUIDE.md](./DATABASE_CLI_GUIDE.md) for full CLI documentation.*
