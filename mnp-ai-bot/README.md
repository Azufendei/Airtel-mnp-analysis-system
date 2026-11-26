# MNP AI Bot - Enterprise Backend API

A high-performance FastAPI backend for analyzing Mobile Number Portability (MNP) journeys, correlating cross-operator telecom logs, synthesizing TRAI compliance insights, and providing enterprise security.

[![Continuous Integration (CI)](https://github.com/Azufendei/Airtel-mnp-analysis-system/actions/workflows/ci.yml/badge.svg)](https://github.com/Azufendei/Airtel-mnp-analysis-system/actions/workflows/ci.yml)

---

## 🎯 Architecture Overview

The backend acts as the core compliance, correlation, and analytics engine for telecom porting events:

```
                      ┌─────────────────────────────────────────┐
                      │    FastAPI Application (Port 8000)      │
                      └──────────────────┬──────────────────────┘
                                         │
                 ┌───────────────────────┼───────────────────────┐
                 ▼                       ▼                       ▼
      ┌─────────────────────┐ ┌─────────────────────┐ ┌─────────────────────┐
      │  OAuth2 / JWT Auth  │ │  Analytics Engine   │ │ SQLAlchemy Pooling  │
      │  • Salted Bcrypt    │ │  • Log Correlation  │ │  • pool_size=10     │
      │  • Role-Based (RBAC)│ │  • TRAI Validation  │ │  • pool_recycle=3600│
      │  • Bearer Token Ver.│ │  • Groq LLM (Qwen)  │ │  • pool_pre_ping    │
      └─────────────────────┘ └─────────────────────┘ └──────────┬──────────┘
                                                                 │
                                                                 ▼
                                                    ┌─────────────────────────┐
                                                    │ PostgreSQL 16 (DB)      │
                                                    │ • user_olm              │
                                                    │ • mnp_journey           │
                                                    │ • application_log       │
                                                    └─────────────────────────┘
```

---

## ✨ Enterprise Features

### 🔐 Security & Access Control
- **OAuth2 Password Grant Flow**: Returns signed JWT Bearer tokens with configurable expiration.
- **Salted Bcrypt Hashing**: Passwords stored using native salted `bcrypt` hashes (no plaintext credentials).
- **Role-Based Access Control (RBAC)**: Fine-grained permissions across `admin`, `tech`, `support`, and `viewer` roles.
- **Protected Analytics Routes**: All sensitive subscriber analysis requires valid bearer authentication.

### 📊 Telecom Journey & Log Correlation
- **Event Lifecycle Tracking**: Tracks `UPC`, `Port_in`, `Port_out`, `NPD_IN`, `NPD_Out`, and `Number_return` events.
- **Log Correlation**: Correlates gateway logs (API, Orchestrator, Database, Gateway) with journey timestamps.
- **TRAI Regulatory Rule Engine**: Automatically evaluates compliance against TRAI standards:
  - Minimum 10-day cooling period before number return
  - Same-circle 4-day porting turnaround limits
  - 15-day Unique Porting Code (UPC) validity windows

### 🤖 LLM Compliance Synthesis & Resilient Fallback
- **Groq Integration**: Powered by `qwen/qwen3.8-27b` with native JSON mode (`response_format={"type": "json_object"}`).
- **Strict Pydantic Validation**: Outputs validated against `AIAnalysisOutput` schemas (root cause, recommendations, warnings, next actions).
- **Deterministic Rule-Based Fallback**: Gracefully operates even when the LLM service is offline or `GROQ_API_KEY` is not provisioned.

### 🗄️ Database Engineering
- **Production Connection Pooling**: Configured with `pool_size=10, max_overflow=20, pool_pre_ping=True, pool_recycle=3600` to prevent stale connection leaks.
- **Relational Integrity**: Foreign keys, composite indexes on `(msisdn, timestamp)`, and cascade configurations.

---

## 📋 Requirements

- **Python**: 3.11+
- **PostgreSQL**: 14+ (16 recommended)
- **OS**: Windows, macOS, Linux

---

## ⚙️ Installation & Setup

### 1. Create Virtual Environment
```bash
cd mnp-ai-bot
python -m venv venv

# Windows (PowerShell)
.\venv\Scripts\Activate.ps1
# Linux / macOS
source venv/bin/activate
```

### 2. Install Dependencies
```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Configure Environment Variables
Create `.env` based on `.env.example`:
```ini
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/mnp_bot_db
SECRET_KEY=your-secure-random-secret-key-at-least-32-chars-long
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
ENVIRONMENT=development
GROQ_API_KEY=gsk_your_groq_api_key_here
GROQ_MODEL=qwen/qwen3.8-27b
```

### 4. Initialize Database
```bash
python setup_db.py
```
This creates all tables, applies indexes, and seeds the enterprise user directory with bcrypt-hashed credentials.

---

## 🧪 Testing Suite (10 Automated Tests)

Run the automated integration test suite:
```bash
python -m pytest -v
```

The suite validates:
1. System health and liveness probe (`/health`)
2. Valid OAuth2 login and token generation (`/auth/login`)
3. Rejection on incorrect password (401)
4. Rejection on unknown OLM ID (401)
5. Bearer token requirement on user profile (`/auth/me`)
6. Token identity resolution (`/auth/me`)
7. Protection of core analytics route (`/analyze` 401 without token)
8. End-to-end journey correlation and structured analysis
9. TRAI 10-day cooling period violation detection
10. Role-based access control (`/users` allows admin, rejects viewer with 403)

---

## 🚀 Running the Server

```bash
# Development mode with hot-reload
uvicorn app.main:app --reload --port 8000

# Production mode
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

- **Swagger Documentation**: `http://localhost:8000/docs`
- **ReDoc Documentation**: `http://localhost:8000/redoc`

---

## 📚 API Endpoints Summary

| Method | Endpoint | Access | Purpose |
|---|---|---|---|
| `POST` | `/auth/login` | Public | Authenticate OLM ID and password, returns JWT token |
| `GET` | `/auth/me` | Bearer Token | Retrieve profile of currently authenticated user |
| `POST` | `/analyze` | Bearer Token | Analyze subscriber journey, gateway logs, & TRAI rules |
| `GET` | `/health` | Public | System liveness probe and version check |
| `GET` | `/users` | Admin / Tech | Directory of registered OLM operators |
| `POST` | `/admin/insert_sample_data` | Dev / Admin | Populate test journey with cooling violation |

*Refer to [QUICK_API_REFERENCE.md](./QUICK_API_REFERENCE.md) for full cURL request/response payloads.*

---

## 📊 Pre-Seeded Enterprise Accounts

| OLM ID | Role | Access Level | Default Password |
|---|---|---|---|
| `OLM_ADMIN_001` | `admin` | Full management access, admin routes | `Password@123` |
| `OLM_TECH_001` | `tech` | Engineering operations, user list | `Password@123` |
| `OLM_SUPPORT_001` | `support` | Subscriber analytics & investigation | `Password@123` |
| `OLM_EXEC_001` | `viewer` | Read-only analytics viewer | `Password@123` |

---

## 📊 Power BI & Local CLI Integration

- **Power BI Reporting**: Connect directly via PostgreSQL connector to build real-time executive dashboards. See [POWERBI_GUIDE.md](./POWERBI_GUIDE.md).
- **Local CLI Management**: Perform schema inspections, database stats, and direct MSISDN lookups with `db_cli.py`. See [DATABASE_CLI_GUIDE.md](./DATABASE_CLI_GUIDE.md).
