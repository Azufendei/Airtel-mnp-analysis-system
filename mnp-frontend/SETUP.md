# MNP Frontend - Quick Setup Guide

## ⚡ Quick Start (5 minutes)

### Step 1: Install Dependencies
```bash
cd mnp-frontend
npm install
```

### Step 2: Configure Backend URL
By default, the app connects to `http://localhost:8000`. If your backend is on a different URL, update `.env`:
```bash
VITE_API_URL=http://your-backend-url:port
```

### Step 3: Start Development Server
```bash
npm run dev
```

The app opens at `http://localhost:3000`

### Step 4: Login
- Use your OLM ID to log in
- For testing, you can use sample OLM IDs from the backend

---

## 🔧 Configuration

### Environment Variables (.env)
```bash
# API Backend URL
VITE_API_URL=http://localhost:8000
```

### Backend Must Be Running
The frontend requires the FastAPI backend to be running:
```bash
# In the mnp-ai-bot directory
python -m uvicorn app.main:app --reload --port 8000
```

---

## 🧪 Testing with Sample Data

### Seed Sample Data
The backend provides an endpoint to insert sample data:
```bash
curl -X POST http://localhost:8000/test/insert_sample_data
```

### Test MSISDNs
After seeding, use these MSISDNs to test:
- `919890123456`
- `919876543210`

### Test OLM IDs
Check available users:
```bash
curl http://localhost:8000/users
```

---

## 📦 Production Build

### Build
```bash
npm run build
```

Output goes to `dist/` directory.

### Preview
```bash
npm run preview
```

### Deploy
The `dist/` folder can be deployed to any static hosting:
- Vercel
- Netlify
- AWS S3
- GitHub Pages
- Any web server

---

## 🐛 Troubleshooting

### Port Already in Use
If port 3000 is already in use:
```bash
# Windows: Kill process on port 3000
netstat -ano | findstr :3000
taskkill /PID <PID> /F

# macOS/Linux
lsof -i :3000
kill -9 <PID>
```

### API Connection Error
1. Verify backend is running: `curl http://localhost:8000/health`
2. Check `.env` file has correct `VITE_API_URL`
3. Check browser DevTools Network tab for failed requests
4. Verify CORS is enabled on backend (it is by default)

### Clear Cache
```bash
# Clear browser cache
localStorage.clear()

# Or delete node_modules and reinstall
rm -rf node_modules
npm install
```

---

## 📱 Mobile Testing

### Access on Other Devices
```bash
# Find your machine's IP
ipconfig getifaddr en0  # macOS
hostname -I             # Linux
ipconfig                # Windows

# Access from mobile on same network
http://<your-ip>:3000
```

---

## 🔐 Security Notes

### Development vs Production
- **Development**: All warnings shown, full error messages
- **Production**: Errors are graceful, no sensitive data exposed

### Session Management
- Sessions stored in `localStorage`
- For production, consider using `sessionStorage` (expires on browser close)
- Implement HTTPS for secure token transmission

---

## 📊 Application Flow

1. **Login** → Enter OLM ID
2. **Search** → Enter MSISDN ± Date Range
3. **Analyze** → API processes request
4. **View Results** → Three tabs:
   - **Journey**: MNP events table
   - **Logs**: Analysis & statistics
   - **Suggestions**: Recommendations
5. **Export/Print** → Download JSON or print results

---

## 🎨 Customization

### Colors
Edit CSS variables in `src/index.css`:
```css
:root {
  --primary: #667eea;
  --secondary: #764ba2;
  --success: #10b981;
  --error: #dc2626;
  /* ... more colors */
}
```

### Fonts
Modify font family in `body` selector in `src/index.css`

### Branding
- Update app title in `index.html`
- Change logo in header (Dashboard.tsx)
- Modify colors in CSS files

---

## 📚 Key Components

| Component | Purpose |
|-----------|---------|
| `App.tsx` | Main app router |
| `Dashboard.tsx` | Main interface |
| `LoginPage.tsx` | Authentication |
| `SearchForm.tsx` | MSISDN input |
| `JourneyTable.tsx` | MNP events display |
| `LogsAnalysis.tsx` | Logs visualization |
| `Suggestions.tsx` | Recommendations |

---

## 🚀 Performance Tips

1. **Optimize Bundle**: `npm run build` creates optimized dist/
2. **Lazy Loading**: Results load on-demand
3. **Caching**: Browser caches API responses
4. **CDN**: Serve dist/ from CDN for faster loading

---

## ❓ FAQ

**Q: How do I change the backend URL?**
A: Edit `.env` file and set `VITE_API_URL`

**Q: Where is session data stored?**
A: In browser's `localStorage` under key `olm_id`

**Q: Can I use this without HTTPS?**
A: Yes for development, but HTTPS recommended for production

**Q: How do I export results?**
A: Click the "Export JSON" button in results page

**Q: Can I print the results?**
A: Yes, click "Print" button or use Ctrl+P

---

## 📞 Support

For issues:
1. Check browser DevTools console
2. Verify backend is running
3. Check `.env` configuration
4. Review README.md for detailed info

---

## 🎯 Next Steps

1. ✅ Install dependencies
2. ✅ Start backend
3. ✅ Start frontend dev server
4. ✅ Test with sample data
5. ✅ Customize branding (optional)
6. ✅ Deploy to production

Happy analyzing! 🚀
