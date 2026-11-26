# Getting Started - MNP Frontend Application

A complete onboarding guide for developers and operators using the MNP Frontend.

---

## ⚡ Quick Start

### 1. Clone & Navigate
```bash
cd mnp-frontend
```

### 2. Install Dependencies
```bash
npm install
```

### 3. Verify Environment Configuration
Copy `.env.example` to `.env` if not already present:
```bash
cp .env.example .env
```
Default configuration:
```ini
VITE_API_URL=http://localhost:8000
```

### 4. Run Development Server
```bash
npm run dev
```

---

## 🔐 Logging In

1. Open your browser at `http://localhost:3000`.
2. Input credentials:
   - **OLM ID**: `OLM_ADMIN_001`
   - **Password**: `Password@123`
3. Click **Sign In**.

---

## 🔍 Exploring Subscriber Journeys

1. In the search bar, enter MSISDN: `919890123456`.
2. Click **Analyze Journey**.
3. View the three synchronized tabs:
   - **MNP Journey**: Chronological event logs with operator, circle, and status.
   - **Logs Analysis**: Gateway error rates, info messages, and visual timeline.
   - **Suggestions**: TRAI regulatory compliance warnings (including 10-day cooling violations) and AI recommendations.
4. Use **Export JSON** or **Print Report** to share findings with support teams.
