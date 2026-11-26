# MNP Frontend - Quick Setup Guide

Follow this guide to get the MNP frontend running on your machine.

---

## 📋 Prerequisites
- **Node.js**: 18+ (tested on Node 20 LTS)
- **Backend API**: Running at `http://localhost:8000`

---

## ⚙️ Step-by-Step Installation

### 1. Install Node Dependencies
```bash
cd mnp-frontend
npm install
```

### 2. Configure Backend API Endpoint
By default, the frontend connects to `http://localhost:8000`. If running on a different port or host, update `.env`:
```ini
VITE_API_URL=http://localhost:8000
```

### 3. Start Development Server
```bash
npm run dev
```
Navigate to `http://localhost:3000` in your browser.

---

## 🔑 Authentication
- Enter any seeded OLM ID (e.g. `OLM_ADMIN_001` or `OLM_SUPPORT_001`).
- Enter the default enterprise password: `Password@123`.
- The frontend securely exchanges credentials for a signed JWT Bearer token and redirects to the analytics dashboard.

---

## 🏗️ Production Build
```bash
npm run build
```
Generates production assets in `dist/` ready for hosting on Vercel, Netlify, AWS S3/CloudFront, or Docker/Nginx.
