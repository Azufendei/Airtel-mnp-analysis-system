# Airtel MNP Analysis & Intelligence System

[![Continuous Integration (CI)](https://github.com/Azufendei/Airtel-mnp-analysis-system/actions/workflows/ci.yml/badge.svg)](https://github.com/Azufendei/Airtel-mnp-analysis-system/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-009688?logo=fastapi)
![React](https://img.shields.io/badge/React-18-61DAFB?logo=react)
![TypeScript](https://img.shields.io/badge/TypeScript-5-3178C6?logo=typescript)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791?logo=postgresql)
![Tests](https://img.shields.io/badge/Tests-10%2F10%20Passing-brightgreen)

An enterprise-grade Mobile Number Portability (MNP) journey analytics and regulatory compliance platform. Built for telecommunications operators to correlate subscriber porting requests across clearinghouse gateways, identify cross-operator dispute bottlenecks, detect **Telecom Regulatory Authority of India (TRAI)** compliance breaches, and synthesize actionable resolution insights with LLM intelligence.

---

## 🏛️ System Architecture

```mermaid
flowchart TD
    subgraph Client ["Frontend (React 18 + TypeScript + Vite)"]
        UI["Operator Dashboard & Search Form"]
        AuthCtx["Auth Context (JWT Storage in localStorage)"]
        Axios["Axios Interceptor (Authorization: Bearer <token>)"]
        UI --> AuthCtx --> Axios
    end

    subgraph Gateway ["Backend API Gateway (FastAPI)"]
        AuthRouter["/auth/login & /auth/me"]
        BcryptHash["Native Salted Bcrypt Hashing"]
        JWTVerify["OAuth2 JWT Bearer Validation"]
        RBAC["Role-Based Access Control (Admin / Tech / Support / Viewer)"]
        AnalyzeEndpoint["POST /analyze"]
        AdminRouter["POST /admin/* (Protected Dev/Admin)"]

        Axios -->|POST /auth/login| AuthRouter
        AuthRouter --> BcryptHash
        Axios -->|POST /analyze (Bearer Token)| JWTVerify
        JWTVerify --> RBAC --> AnalyzeEndpoint
    end

    subgraph Core ["Analytics & Compliance Core"]
        LogCorr["Gateway Log Correlation Engine"]
        TRAIEngine["TRAI Regulatory Engine\n• 10-day Cooling Period Check\n• 4-day Porting SLA Window\n• 15-day UPC Validity Window"]
        LLM["Groq LLM Engine (qwen/qwen3.8-27b)\n• JSON Mode\n• Pydantic AIAnalysisOutput"]
        RuleFallback["Deterministic Rule-Based Fallback"]

        AnalyzeEndpoint --> LogCorr
        AnalyzeEndpoint --> TRAIEngine
        TRAIEngine --> LLM
        LLM -.->|On Timeout or Offline| RuleFallback
    end

    subgraph Data ["Database Tier (PostgreSQL 16)"]
        Pool["SQLAlchemy Connection Pool\n(pool_size=10, max_overflow=20, pre_ping=True)"]
        DB[("PostgreSQL DB\n• user_olm\n• mnp_journey\n• application_log")]

        Gateway --> Pool --> DB
        LogCorr --> Pool
    end

    subgraph BI ["Reporting Tier"]
        PowerBI["Power BI Desktop (Direct PostgreSQL Connector)"]
        DB -.-> PowerBI
    end
```

---

## 🚀 Key Production Capabilities

### 1. Enterprise Security & RBAC
- **OAuth2 Password Grant**: Standardized `POST /auth/login` exchanging OLM ID and password for signed HMAC-SHA256 JWT tokens.
- **Bcrypt Password Security**: Native salted `bcrypt` password hashing (no plaintext passwords).
- **Role-Based Permissions**: Granular roles (`admin`, `tech`, `support`, `viewer`) enforced via FastAPI route dependencies.
- **Client Interceptors**: Axios interceptors automatically attach `Authorization: Bearer` headers and intercept `401 Unauthorized` responses to redirect expired sessions.

### 2. TRAI Telecom Regulatory Engine
- **10-Day Cooling Period Rule**: Automatically detects when a number return is initiated within 10 days of a successful port-in, flagging a critical regulatory non-compliance alert.
- **Same-Circle Porting Window**: Evaluates same-circle porting requests against the mandatory 4-working-day completion SLA.
- **UPC Expiration Tracking**: Tracks 15-day Unique Porting Code (UPC) validity across clearinghouse logs.

### 3. Resilient AI & Structured Outputs
- **Groq LLM Synthesis**: Powered by `qwen/qwen3.8-27b` using native JSON mode to generate structured root-cause analysis and prioritized recommendations.
- **Pydantic Validation**: All LLM outputs are validated against the strict `AIAnalysisOutput` schema before returning to the client.
- **Zero-Failure Fallback**: If the LLM provider is offline or `GROQ_API_KEY` is omitted, the engine automatically falls back to deterministic rule-based algorithms.

### 4. Database Reliability
- **Connection Pooling**: Managed SQLAlchemy connection pool (`pool_size=10, max_overflow=20, pool_pre_ping=True, pool_recycle=3600`) to prevent stale socket leaks.
- **Optimized Queries**: Composite indexing on `(msisdn, timestamp)` for high-throughput subscriber lookups.

### 5. Automated CI/CD
- **GitHub Actions Dual Pipeline**: Every push and PR triggers automated testing across isolated containers:
  - **Frontend**: Node 20 environment running strict TypeScript typechecking and Vite production compilation.
  - **Backend**: Python 3.11 environment with an isolated PostgreSQL 16 Alpine service container running database bootstrapping and the full 10-test integration suite.

---

## 👥 Seeded Enterprise Accounts

The database bootstrapping script (`setup_db.py`) automatically provisions the following accounts:

| OLM ID | Role | Access Level | Default Password |
|---|---|---|---|
| `OLM_ADMIN_001` | `admin` | Full management access, admin routes | `Password@123` |
| `OLM_TECH_001` | `tech` | Engineering operations, user list | `Password@123` |
| `OLM_SUPPORT_001` | `support` | Subscriber analytics & investigation | `Password@123` |
| `OLM_EXEC_001` | `viewer` | Read-only analytics viewer | `Password@123` |

---

## ⚡ Quick Start

### 1. Prerequisites
- **Python**: 3.11+
- **Node.js**: 18+ (Node 20 recommended)
- **PostgreSQL**: 14+ (or Docker container)

---

### 2. Backend Setup (Terminal 1)

```bash
cd mnp-ai-bot

# 1. Create and activate virtual environment
python -m venv venv
# Windows (PowerShell):
.\venv\Scripts\Activate.ps1
# Linux / macOS:
source venv/bin/activate

# 2. Install dependencies
python -m pip install --upgrade pip
pip install -r requirements.txt

# 3. Configure environment
cp .env.example .env
# Edit .env with your PostgreSQL credentials:
# DATABASE_URL=postgresql://postgres:your_password@localhost:5432/mnp_bot_db

# 4. Bootstrap tables and seed enterprise users
python setup_db.py

# 5. Run automated test suite (10/10 tests)
python -m pytest -v

# 6. Start development server
uvicorn app.main:app --reload --port 8000
```
API Documentation will be live at: **`http://localhost:8000/docs`**

---

### 3. Frontend Setup (Terminal 2)

```bash
cd mnp-frontend

# 1. Install dependencies
npm install

# 2. Verify backend URL in .env
# VITE_API_URL=http://localhost:8000

# 3. Start development server
npm run dev
```
Application will be live at: **`http://localhost:3000`**

---

## 🧪 Testing the Subscriber Journey

1. Open **`http://localhost:3000`** in your browser.
2. Sign in with:
   - **OLM ID**: `OLM_ADMIN_001`
   - **Password**: `Password@123`
3. Enter test subscriber MSISDN:
   - **`919890123456`**: Populates a multi-event journey (`Port_in` -> `NPD_IN` -> `Number_return`) triggering the critical TRAI 10-day cooling period breach.
   - **`919876543210`**: Standard port-out journey across circles.
4. Inspect the 3 synchronized tabs:
   - **MNP Journey**: Chronological event logs with operators (Jio, Airtel), circles, and transaction IDs.
   - **Logs Analysis**: Correlated gateway error counts, warning rates, and daily timeline distribution.
   - **Suggestions**: TRAI regulatory compliance warnings and AI recommendations.
5. Export results as JSON or print the executive summary.

---

## 📚 API Endpoints Summary

| Method | Route | Auth | Description |
|---|---|---|---|
| `POST` | `/auth/login` | Public | Authenticates credentials, returns signed JWT Bearer token |
| `GET` | `/auth/me` | Bearer | Resolves identity and role of active session |
| `POST` | `/analyze` | Bearer | Analyzes subscriber journey, gateway logs, & TRAI rules |
| `GET` | `/health` | Public | Liveness probe returning status, version, and environment |
| `GET` | `/users` | Admin/Tech | Lists registered OLM operators (RBAC guarded) |
| `POST` | `/admin/insert_sample_data` | Dev/Admin | Seeds test journey containing TRAI cooling violation |

*Refer to [mnp-ai-bot/QUICK_API_REFERENCE.md](file:///c:/Users/gupta/Desktop/RandomProjects/mnp-ai-bot/QUICK_API_REFERENCE.md) for full request & response payloads.*

---

## 📊 Power BI Desktop Integration

The PostgreSQL database supports direct connectivity with **Power BI Desktop** for real-time executive dashboarding:
- Connect using the native PostgreSQL connector (`Server: localhost`, `Database: mnp_bot_db`).
- Load `mnp_journey`, `application_log`, and `user_olm` tables.
- Visualize operator port-in vs. port-out ratios, rejection distributions, and circle-level performance.
- Detailed step-by-step setup in [mnp-ai-bot/POWERBI_GUIDE.md](file:///c:/Users/gupta/Desktop/RandomProjects/mnp-ai-bot/POWERBI_GUIDE.md).

---

## 📁 Repository Structure

```
Airtel-mnp-analysis-system/
├── .github/
│   └── workflows/
│       └── ci.yml               # Dual CI pipeline (PostgreSQL 16 + Node 20)
├── mnp-ai-bot/                  # FastAPI Backend Service
│   ├── app/
│   │   ├── main.py              # Application entrypoint & routes
│   │   ├── auth.py              # Bcrypt hashing & JWT token verification
│   │   ├── models.py            # SQLAlchemy database models
│   │   ├── schemas.py           # Pydantic schemas (AIAnalysisOutput)
│   │   ├── database.py          # SQLAlchemy connection pooling
│   │   ├── mnp_analyzer.py      # TRAI compliance & Groq AI engine
│   │   └── config.py            # Environment configurations
│   ├── tests/
│   │   └── test_endpoints.py    # 10 integration & compliance tests
│   ├── setup_db.py              # Database migration & user seeding
│   ├── db_cli.py                # Local database management CLI
│   ├── pytest.ini               # Pytest configuration
│   └── requirements.txt         # Pinned backend dependencies
├── mnp-frontend/                # React 18 + TypeScript Frontend
│   ├── src/
│   │   ├── main.tsx             # Application mount point
│   │   ├── App.tsx              # View router
│   │   ├── AuthContext.tsx      # JWT session & Axios interceptors
│   │   ├── ProtectedRoute.tsx   # Authenticated route guard
│   │   ├── LoginPage.tsx        # Enterprise login UI
│   │   ├── Dashboard.tsx        # Analytics workspace
│   │   ├── SearchForm.tsx       # Subscriber input form
│   │   ├── JourneyTable.tsx     # Tabular journey visualizer
│   │   ├── LogsAnalysis.tsx     # Log correlation & timeline chart
│   │   ├── Suggestions.tsx      # TRAI compliance & AI suggestions
│   │   ├── api.ts               # Axios client
│   │   └── types.ts             # TypeScript interface contracts
│   ├── index.html               # Single page shell
│   └── package.json             # Frontend dependencies
├── .gitignore                   # Multi-tier ignore rules
└── README.md                    # Project overview & architecture
```

---

## 📜 License

Proprietary — Airtel MNP Analysis System. Built for enterprise telecom operations.
