# Getting Started - MNP AI Bot Backend

A comprehensive guide to set up, test, and run the enterprise MNP AI Bot backend locally.

---

## ⚡ Quick Start (5 Minutes)

### Prerequisites
- **Python**: 3.11+ installed
- **PostgreSQL**: 14+ running locally (or via Docker)
- **Virtualenv**: Python virtual environment tooling

---

### 1. Setup Virtual Environment

```bash
cd mnp-ai-bot

# Create isolated virtual environment
python -m venv venv

# Activate virtual environment
# Windows (PowerShell):
.\venv\Scripts\Activate.ps1
# Windows (cmd.exe):
venv\Scripts\activate.bat
# Linux / macOS:
source venv/bin/activate
```

---

### 2. Install Dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

---

### 3. Configure Environment Variables

Copy the example `.env` template:
```bash
cp .env.example .env
```

Verify/update `.env` configurations:
```ini
# PostgreSQL Connection URL
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/mnp_bot_db

# Security & JWT Tokens
SECRET_KEY=your-secure-random-secret-key-at-least-32-chars-long
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
ENVIRONMENT=development

# Groq LLM Inference (TRAI compliance synthesis)
GROQ_API_KEY=gsk_your_groq_api_key_here
GROQ_MODEL=qwen/qwen3.8-27b
```
*(Note: If `GROQ_API_KEY` is omitted, the system automatically falls back to deterministic rule-based TRAI suggestions without throwing errors).*

---

### 4. Bootstrap Database & Seed Enterprise Users

Execute the database bootstrapping script to create all relational tables (`user_olm`, `mnp_journey`, `application_log`), configure indexes, and seed initial enterprise accounts:

```bash
python setup_db.py
```

**Default Seeded Accounts**:
- `OLM_ADMIN_001` (Role: `admin`) | Password: `Password@123`
- `OLM_TECH_001` (Role: `tech`) | Password: `Password@123`
- `OLM_SUPPORT_001` (Role: `support`) | Password: `Password@123`
- `OLM_EXEC_001` (Role: `viewer`) | Password: `Password@123`

---

### 5. Run Automated Test Suite

Verify that all 10 automated unit and integration tests pass:

```bash
python -m pytest -v
```

Expected output:
```
tests/test_endpoints.py::test_health_endpoint PASSED                     [ 10%]
tests/test_endpoints.py::test_auth_login_success PASSED                  [ 20%]
tests/test_endpoints.py::test_auth_login_invalid_password PASSED         [ 30%]
tests/test_endpoints.py::test_auth_login_nonexistent_user PASSED         [ 40%]
tests/test_endpoints.py::test_auth_me_unauthorized PASSED                [ 50%]
tests/test_endpoints.py::test_auth_me_authorized PASSED                  [ 60%]
tests/test_endpoints.py::test_analyze_unauthorized PASSED                [ 70%]
tests/test_endpoints.py::test_analyze_authorized PASSED                  [ 80%]
tests/test_endpoints.py::test_trai_cooling_period_violation_detection PASSED [ 90%]
tests/test_endpoints.py::test_role_based_access_control PASSED           [100%]

============================= 10 passed =============================
```

---

### 6. Start API Server

```bash
uvicorn app.main:app --reload --port 8000
```

- **API Base URL**: `http://localhost:8000`
- **Interactive Swagger UI**: `http://localhost:8000/docs`
- **ReDoc UI**: `http://localhost:8000/redoc`

---

## 🧪 Testing the API Locally

### 1. Check Liveness
```bash
curl http://localhost:8000/health
```

### 2. Populate Test Data
```bash
curl -X POST http://localhost:8000/admin/insert_sample_data
```

### 3. Log In & Obtain Token
```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"olm_id": "OLM_ADMIN_001", "password": "Password@123"}'
```

### 4. Analyze MNP Journey
```bash
TOKEN="<paste_access_token_from_login>"

curl -X POST http://localhost:8000/analyze \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"msisdn": "919890123456"}'
```

---

## 🛠️ Local Database Management (CLI)

For administrative batch updates, queries, and diagnostics without exposing public API routes:

```bash
# Summary statistics
python db_cli.py stats

# Query journey records by subscriber MSISDN
python db_cli.py query mnp_journey --msisdn 919890123456

# Review table structure
python db_cli.py structure mnp_journey
```
*Refer to [DATABASE_CLI_GUIDE.md](./DATABASE_CLI_GUIDE.md) for complete CLI commands.*
