# ⚡ MNP Frontend - Quick Reference Guide

## 🚀 3-Minute Setup

### Step 1: Install Dependencies
```bash
cd mnp-frontend
npm install
```

### Step 2: Verify Backend URL
Ensure `.env` contains:
```ini
VITE_API_URL=http://localhost:8000
```

### Step 3: Launch Frontend
```bash
npm run dev
```
Open **`http://localhost:3000`** in your browser.

---

## 🔐 Login Credentials

| OLM ID | Role | Password |
|---|---|---|
| `OLM_ADMIN_001` | Admin | `Password@123` |
| `OLM_TECH_001` | Tech | `Password@123` |
| `OLM_SUPPORT_001`| Support | `Password@123` |
| `OLM_EXEC_001` | Viewer | `Password@123` |

---

## 🔍 Test Subscribers

1. **MSISDN**: `919890123456`
   - Demonstrates: Port-in, NPD IN, and Number Return events.
   - Triggers: Critical TRAI 10-day cooling period warning.
2. **MSISDN**: `919876543210`
   - Demonstrates: Port-out event with transaction code.

---

## 🛠️ Common Commands

```bash
# Start local dev server with hot reload
npm run dev

# Run strict TypeScript type check and production build
npm run build

# Preview production build locally
npm run preview
```
