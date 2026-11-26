# MNP Frontend - Enterprise React Application

A modern, responsive React 18 + TypeScript single-page application (SPA) for analyzing Mobile Number Portability (MNP) journeys, visualizing cross-operator gateway logs, and inspecting TRAI compliance insights with AI synthesis.

[![Continuous Integration (CI)](https://github.com/Azufendei/Airtel-mnp-analysis-system/actions/workflows/ci.yml/badge.svg)](https://github.com/Azufendei/Airtel-mnp-analysis-system/actions/workflows/ci.yml)

---

## 🎯 Application Overview

The frontend connects to the FastAPI backend with enterprise OAuth2/JWT Bearer authentication to deliver:
- **Secure Authentication**: OLM ID & password login with JWT token storage in `localStorage`.
- **Axios Interceptor**: Automatically attaches `Authorization: Bearer <token>` to outbound API requests and intercepts `401 Unauthorized` responses to seamlessly redirect expired sessions to the login view.
- **Role Badges & RBAC**: Dynamic role indicator badge (`admin`, `tech`, `support`, `viewer`).
- **Interactive Subscriber Search**: 10-13 digit MSISDN validation with optional date range filters.
- **Tabular Journey Visualization**: Chronological event tracking (`UPC`, `Port_in`, `Port_out`, `NPD_IN`, `NPD_Out`, `Number_return`) with status badges and expandable metadata.
- **Gateway Log Diagnostics**: Error/warning/info counters, timeline event charts, and root-cause issue detection.
- **TRAI Compliance & AI Suggestions**: Categorized severity cards (`critical`, `high`, `medium`, `low`) highlighting cooling period breaches and actionable next steps.
- **Export & Print**: One-click JSON data export and print-optimized executive styling.

---

## 🔐 Seeded Demo Accounts

The backend pre-seeds the following enterprise accounts (passwords hashed with `bcrypt`):

| OLM ID | Role | Access Level | Default Password |
|---|---|---|---|
| `OLM_ADMIN_001` | `admin` | Full system access & user management | `Password@123` |
| `OLM_TECH_001` | `tech` | Engineering operations & user directory | `Password@123` |
| `OLM_SUPPORT_001`| `support` | Subscriber journey lookup & resolution | `Password@123` |
| `OLM_EXEC_001` | `viewer` | Read-only analytics viewer | `Password@123` |

---

## ⚡ Quick Start

### Prerequisites
- **Node.js**: 18+ (Node 20 recommended)
- **npm**: 9+
- **Backend**: FastAPI backend running on `http://localhost:8000`

### 1. Install Dependencies
```bash
cd mnp-frontend
npm install
```

### 2. Configure Environment
Verify `.env` (copied from `.env.example`):
```ini
VITE_API_URL=http://localhost:8000
```

### 3. Start Development Server
```bash
npm run dev
```
The application will launch at: **`http://localhost:3000`** (or Vite default port `5173`).

### 4. Build for Production & Typecheck
```bash
npm run build
```
Executes TypeScript compilation (`tsc`) and Vite bundling (`vite build`) producing an optimized distribution bundle in `dist/`.

---

## 📁 Source Code Structure

```
mnp-frontend/
├── index.html                   # HTML5 shell entry
├── package.json                 # Dependencies & build scripts
├── tsconfig.json                # TypeScript compiler config
├── vite.config.ts               # Vite bundler & port config
├── public/                      # Static assets and icons
└── src/
    ├── main.tsx                 # React DOM mount entry
    ├── App.tsx                  # Root component & view routing
    ├── AuthContext.tsx          # JWT auth state & token interceptors
    ├── ProtectedRoute.tsx       # Route protection wrapper
    ├── LoginPage.tsx            # OLM ID & password login form
    ├── Dashboard.tsx            # Central analytics workspace
    ├── SearchForm.tsx           # MSISDN search & date range input
    ├── JourneyTable.tsx         # Tabular MNP journey event view
    ├── LogsAnalysis.tsx         # Gateway log timeline & error metrics
    ├── Suggestions.tsx          # TRAI compliance & AI suggestions cards
    ├── api.ts                   # Axios client with Bearer interceptors
    ├── types.ts                 # Full-stack TypeScript interfaces
    └── *.css                    # Component-scoped styling
```

---

## 🧪 Testing Subscriber Numbers

For instant verification with sample data (pre-populated by backend `/admin/insert_sample_data`):
- **MSISDN**: `919890123456` (Contains sample journey with a 2-day return cooling period violation)
- **MSISDN**: `919876543210` (Standard port-out journey)
