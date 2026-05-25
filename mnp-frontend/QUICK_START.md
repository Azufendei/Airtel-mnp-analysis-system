# ⚡ MNP Frontend - Quick Reference

## 🚀 START HERE - 5 Minute Setup

### Step 1: Install
```bash
cd mnp-frontend
npm install
```

### Step 2: Start
```bash
npm run dev
```

### Step 3: Open
```
http://localhost:3000
```

### Step 4: Login
Use any valid OLM ID

---

## 📱 Main Features

### 1. Login 🔐
- Enter OLM ID
- Auto-saves session

### 2. Search 🔍
- Enter MSISDN
- Optional date range
- Auto validates

### 3. View Results 📊
- **Journey Tab**: MNP events table
- **Logs Tab**: Analysis & stats
- **Suggestions Tab**: Recommendations

### 4. Export 💾
- JSON download
- Print view
- Shareable reports

---

## 🎯 Key Endpoints

```
POST /analyze
├── Input: msisdn, olm_id, start_time (opt), end_time (opt)
└── Output: journey, logs_analysis, suggestions

GET /health
└── Check API status

GET /users
└── List all OLM IDs

POST /test/insert_sample_data
└── Load sample data for testing
```

---

## 🗂️ Project Structure

```
src/
├── Components (9 files)
│   ├── App.tsx
│   ├── Dashboard.tsx
│   ├── LoginPage.tsx
│   ├── AuthContext.tsx
│   ├── SearchForm.tsx
│   ├── JourneyTable.tsx
│   ├── LogsAnalysis.tsx
│   └── Suggestions.tsx
├── Services (2 files)
│   ├── api.ts
│   └── types.ts
└── Styles (8 files)
    ├── index.css
    ├── Dashboard.css
    ├── LoginPage.css
    └── ... (more)
```

---

## 🔧 Common Commands

```bash
# Development
npm run dev              # Start dev server
npm run build           # Build for production
npm run preview         # Preview production build

# Utilities
npm list               # Show dependencies
npm update             # Update packages
npm audit              # Check security
```

---

## 🎨 Color Palette

```css
Primary:    #667eea (Purple)
Secondary:  #764ba2 (Dark Purple)
Success:    #10b981 (Green)
Error:      #dc2626 (Red)
Warning:    #f59e0b (Amber)
```

---

## 📲 Responsive Design

| Device | Width | Features |
|--------|-------|----------|
| Mobile | <768px | Stacked layout, touch-friendly |
| Tablet | 768-1199px | 2-column layout |
| Desktop | 1200px+ | Full 3-column layout |

---

## 🔐 Authentication

```
OLM ID (Username)
    ↓
Store in localStorage
    ↓
Auto-restore on refresh
    ↓
Protected routes
    ↓
Auto-logout on 401
```

---

## 🌐 API Communication

```
Frontend Form
    ↓
axios.post('/analyze', data)
    ↓
Backend Processing
    ↓
JSON Response
    ↓
Display Results
    ↓
Export/Print
```

---

## 📊 Data Display Tabs

### Journey Tab 📋
- Event type with icon
- Timestamp
- Operator & circle
- Success/failed status
- Transaction ID
- Expandable details

### Logs Tab 📝
- Total logs count
- Error count
- Warning count
- Info count
- Key issues list
- Timeline chart

### Suggestions Tab 💡
- Grouped by category
- Color-coded priority
- Expandable details
- Legend showing priorities

---

## 🧪 Test Credentials

```bash
# Get sample users
curl http://localhost:8000/users

# Insert sample data
curl -X POST http://localhost:8000/test/insert_sample_data

# Test MSISDNs
919890123456
919876543210
```

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| Port 3000 in use | Kill: `taskkill /PID <PID> /F` |
| API not found | Check backend running |
| Login failed | Verify OLM ID exists |
| Blank page | Clear cache: `Ctrl+Shift+Del` |
| Build error | Delete node_modules, reinstall |

---

## 📈 Performance Tips

- Narrow date ranges load faster
- Use modern browsers
- Enable browser cache
- Deploy with CDN
- Use gzip compression

---

## 🔒 Security Checklist

- ✅ HTTPS in production
- ✅ API URL in .env
- ✅ No hardcoded secrets
- ✅ Input validation
- ✅ Error handling
- ✅ CORS configured

---

## 📚 Documentation Files

| File | Purpose | Read Time |
|------|---------|-----------|
| SETUP.md | Quick start | 5 min |
| README.md | Full docs | 10 min |
| FEATURES.md | Details | 10 min |
| DEPLOYMENT.md | Deploy | 15 min |
| FILE_LIST.md | Files | 5 min |

---

## 🚀 Deployment (Quick)

```bash
# Production build
npm run build

# Deploy dist/ folder to:
# - Vercel: `vercel --prod`
# - Netlify: `netlify deploy --prod`
# - AWS S3: `aws s3 sync dist/ s3://bucket/`
```

---

## 💻 Tech Stack Quick Look

| Layer | Tech | Version |
|-------|------|---------|
| UI | React | 18.2+ |
| Language | TypeScript | 5.2+ |
| Build | Vite | 5.0+ |
| HTTP | Axios | 1.6+ |
| Dates | date-fns | 2.30+ |
| Styling | CSS3 | Latest |

---

## 🎯 Development Workflow

1. **Start Dev Server**: `npm run dev`
2. **Code Changes**: Edit files (auto-reload)
3. **Test Features**: Check browser
4. **Debug**: DevTools > Console/Network
5. **Build**: `npm run build`
6. **Deploy**: Follow DEPLOYMENT.md

---

## 🌟 Key Files to Know

| File | What It Does |
|------|-------------|
| `Dashboard.tsx` | Main UI layout |
| `api.ts` | Backend communication |
| `AuthContext.tsx` | User session |
| `SearchForm.tsx` | Input form |
| `JourneyTable.tsx` | Events display |
| `Dashboard.css` | Main styling |

---

## 📞 Quick Help

```
Login Issue?       → Check OLM ID in backend
API Issue?         → Verify backend running
Style Issue?       → Clear cache, reload
Build Issue?       → npm install again
Performance?       → Narrow date range
Mobile Issue?      → Test in DevTools
```

---

## ✅ Feature Checklist

- ✅ OLM ID Authentication
- ✅ MSISDN Search
- ✅ Date Range Filtering
- ✅ MNP Journey Table
- ✅ Logs Analysis
- ✅ Suggestions/Recommendations
- ✅ Export to JSON
- ✅ Print View
- ✅ Responsive Design
- ✅ Error Handling

---

## 🎉 Ready? Let's Go!

```bash
# Do this NOW:
cd mnp-frontend
npm install
npm run dev

# Then:
1. Open http://localhost:3000
2. Login with OLM ID
3. Search for MSISDN
4. Enjoy! 🎊
```

---

**Version**: 1.0.0
**Framework**: React + TypeScript
**Status**: ✅ Production Ready

More help? Check the full docs in README.md!
