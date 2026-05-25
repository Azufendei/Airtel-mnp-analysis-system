# Getting Started - MNP Frontend

A quick guide to set up and run the MNP Frontend application locally.

## ⚡ Quick Start (5 minutes)

### Prerequisites
- Node.js 16+ and npm 8+ installed
- Backend API running on `http://localhost:8000`

### 1. Install Dependencies
```bash
cd mnp-frontend
npm install
```

### 2. Configure Environment
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env if needed (default works for local development)
# VITE_API_URL=http://localhost:8000
```

### 3. Start Development Server
```bash
npm run dev
```

The app will be available at: **http://localhost:3000**

## 🔐 Environment Setup

### Development (.env)
```
VITE_API_URL=http://localhost:8000
```

### Production Build
```bash
npm run build
npm run preview
```

## 🚀 Available Commands

```bash
# Development server with hot reload
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Type checking
npx tsc --noEmit
```

## 📝 Project Structure

```
src/
├── App.tsx              # Main app component
├── Dashboard.tsx        # Main dashboard
├── LoginPage.tsx        # Login interface
├── AuthContext.tsx      # Auth management
├── SearchForm.tsx       # Search component
├── JourneyTable.tsx     # Results table
├── LogsAnalysis.tsx     # Logs visualization
├── Suggestions.tsx      # Suggestions panel
├── api.ts              # API client
├── types.ts            # TypeScript types
└── [component].css     # Styles
```

## 🧪 Testing the App

1. Start the backend first (see backend README)
2. Start the frontend: `npm run dev`
3. Open http://localhost:3000
4. Login with OLM ID (default: USER001)
5. Search for MSISDN: 919890123456
6. View results in tabs

## ⚠️ Troubleshooting

### Port 3000 Already in Use
```bash
# Find and kill process on port 3000
# Windows
netstat -ano | findstr :3000
taskkill /PID <PID> /F

# macOS/Linux
lsof -i :3000
kill -9 <PID>
```

### API Connection Error
- Verify backend is running: `curl http://localhost:8000/health`
- Check VITE_API_URL in .env
- Check browser console (F12) for CORS errors

### Module Not Found
```bash
rm -rf node_modules package-lock.json
npm install
```

## 📚 For More Information

- See [README.md](./README.md) for detailed documentation
- Backend setup: See [../mnp-ai-bot/README.md](../mnp-ai-bot/README.md)
- API documentation: http://localhost:8000/docs
