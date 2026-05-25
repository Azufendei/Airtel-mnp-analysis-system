# MNP Frontend - Deployment Guide

## 🚀 Production Deployment

This guide covers deploying the MNP Frontend to various hosting platforms.

---

## 📋 Pre-Deployment Checklist

- [ ] Update `.env` with production API URL
- [ ] Run `npm run build` successfully
- [ ] Test `npm run preview` locally
- [ ] All tests pass
- [ ] No console errors or warnings
- [ ] API backend is deployed and accessible

---

## 🏗️ Build for Production

### Generate Optimized Bundle
```bash
npm run build
```

This creates an optimized `dist/` folder (~250KB gzipped).

### Verify Build
```bash
npm run preview
# Opens local preview of production build
```

---

## ☁️ Deployment Platforms

### 1️⃣ Vercel (Recommended - Free)

**Easiest deployment option!**

#### Via CLI:
```bash
npm install -g vercel
vercel
# Follow prompts
# Vercel detects Vite and builds automatically
```

#### Via GitHub:
1. Push code to GitHub
2. Go to [vercel.com](https://vercel.com)
3. Click "New Project"
4. Import your GitHub repository
5. Configure environment: `VITE_API_URL`
6. Deploy!

#### Environment Setup:
```
VITE_API_URL=https://api.your-domain.com
```

---

### 2️⃣ Netlify (Free)

#### Via CLI:
```bash
npm install -g netlify-cli
netlify deploy --prod --dir=dist
```

#### Via GitHub:
1. Go to [netlify.com](https://netlify.com)
2. Click "New site from Git"
3. Choose GitHub repository
4. Build settings:
   - Build command: `npm run build`
   - Publish directory: `dist`
5. Add environment variable: `VITE_API_URL`
6. Deploy!

---

### 3️⃣ AWS S3 + CloudFront

#### Prerequisites:
- AWS account
- AWS CLI installed
- S3 bucket created

#### Deploy:
```bash
# Build
npm run build

# Sync to S3
aws s3 sync dist/ s3://your-bucket-name --delete

# Create CloudFront distribution for CDN (optional)
# See AWS documentation for details
```

#### Configure CloudFront:
- Set origin to S3 bucket
- Enable caching
- Set TTL: 3600 seconds
- Add header for SPA routing

---

### 4️⃣ GitHub Pages (Free for Public Repos)

#### Setup:
```bash
# Update vite.config.ts:
# export default defineConfig({
#   base: '/mnp-frontend/'  // if repo is named mnp-frontend
# })

npm run build
git add dist
git commit -m "Build for deployment"
git push
```

#### Configure GitHub:
1. Go to repo Settings → Pages
2. Source: Deploy from a branch
3. Branch: main, folder: /root or /docs
4. Add `dist/` to github pages

---

### 5️⃣ Docker + Container

#### Create Dockerfile:
```dockerfile
# Build stage
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# Production stage
FROM node:18-alpine
WORKDIR /app
RUN npm install -g serve
COPY --from=builder /app/dist ./dist
EXPOSE 3000
CMD ["serve", "-s", "dist", "-l", "3000"]
```

#### Build & Run:
```bash
docker build -t mnp-frontend .
docker run -p 3000:8080 \
  -e VITE_API_URL=http://api.example.com \
  mnp-frontend
```

---

### 6️⃣ Traditional Web Server (Apache/Nginx)

#### Nginx Configuration:
```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    root /var/www/mnp-frontend/dist;
    index index.html;
    
    # SPA routing: serve index.html for all non-file requests
    location / {
        try_files $uri $uri/ /index.html;
    }
    
    # Cache static assets
    location ~* \.(js|css|png|jpg|svg)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
    
    # API proxy (optional)
    location /api/ {
        proxy_pass http://backend-api:8000/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

#### Apache Configuration:
```apache
<VirtualHost *:80>
    ServerName your-domain.com
    DocumentRoot /var/www/mnp-frontend/dist
    
    # Enable mod_rewrite
    <Directory /var/www/mnp-frontend/dist>
        RewriteEngine On
        RewriteBase /
        RewriteRule ^index\.html$ - [L]
        RewriteCond %{REQUEST_FILENAME} !-f
        RewriteCond %{REQUEST_FILENAME} !-d
        RewriteRule . /index.html [L]
    </Directory>
</VirtualHost>
```

---

## 🌐 Environment Configuration

### Development
```
VITE_API_URL=http://localhost:8000
```

### Staging
```
VITE_API_URL=https://staging-api.example.com
```

### Production
```
VITE_API_URL=https://api.example.com
```

### Set Environment:
```bash
# Create production .env
echo "VITE_API_URL=https://api.example.com" > .env.production

# Build with production env
npm run build
```

---

## 🔒 Security Best Practices

### 1. HTTPS Only
- Always use HTTPS in production
- Get SSL certificate (free via Let's Encrypt)
- Redirect HTTP to HTTPS

### 2. CORS Configuration
- Restrict API origins
- Don't use `allow_origins=["*"]` in production
- Configure backend to accept only your domain

### 3. Environment Variables
- Never commit `.env` to git
- Use platform-specific secrets management
- Rotate API keys regularly

### 4. Headers
```nginx
# Security headers
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-Content-Type-Options "nosniff" always;
add_header X-XSS-Protection "1; mode=block" always;
add_header Referrer-Policy "no-referrer-when-downgrade" always;
add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline';" always;
```

### 5. API Security
- Implement rate limiting on backend
- Add request authentication
- Validate all inputs
- Use API keys for sensitive endpoints

---

## 📊 Performance Optimization

### Enable Compression
```nginx
# Nginx
gzip on;
gzip_types text/plain text/css text/javascript application/json;
gzip_min_length 1000;
```

### Cache Strategy
```nginx
# Cache static assets long-term
location ~* \.(js|css|png|jpg|svg|woff)$ {
    expires 365d;
    add_header Cache-Control "public, immutable";
}

# Don't cache HTML (index.html)
location = /index.html {
    add_header Cache-Control "public, max-age=0, must-revalidate";
}
```

### CDN Setup
- Use CloudFlare or similar CDN
- Cache static assets
- DDoS protection
- Automatic HTTPS

---

## ✅ Post-Deployment Testing

### 1. Functional Testing
```bash
# Test all user flows
- [ ] Login works
- [ ] Search works
- [ ] Results display correctly
- [ ] Export/Print works
- [ ] Logout works
```

### 2. Performance Testing
```bash
# Use Chrome DevTools
- Lighthouse audit (target: 85+)
- Performance tab
- Network analysis
- Bundle size check
```

### 3. Security Testing
```bash
# Security headers check
curl -I https://your-domain.com
# Should see security headers

# SSL test
# Go to https://www.ssllabs.com/ssltest/
```

### 4. Monitoring
- Set up error tracking (Sentry, LogRocket)
- Monitor API response times
- Track user analytics
- Set up uptime monitoring

---

## 🔄 Continuous Deployment

### GitHub Actions Example
```yaml
name: Deploy

on:
  push:
    branches: [ main ]

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-node@v2
        with:
          node-version: '18'
      
      - run: npm install
      - run: npm run build
      
      - name: Deploy to Vercel
        run: npm install -g vercel && vercel --prod --token ${{ secrets.VERCEL_TOKEN }}
```

---

## 🚨 Troubleshooting

### Blank Page After Deploy
- Check browser console for errors
- Verify API URL is correct
- Check CORS settings on backend
- Clear browser cache (Ctrl+Shift+Del)

### 404 Errors on Refresh
- Configure SPA routing (serve index.html for all routes)
- Check web server configuration
- Verify file permissions

### API Connection Failed
- Verify API URL in environment variables
- Check backend is running and accessible
- Verify CORS headers on backend
- Check firewall rules

### Slow Performance
- Enable gzip compression
- Enable caching headers
- Use CDN
- Check database query performance
- Monitor API response times

---

## 📞 Support & Resources

- [Vite Deployment Guide](https://vitejs.dev/guide/static-deploy.html)
- [Vercel Deployment](https://vercel.com/docs)
- [Netlify Deployment](https://docs.netlify.com/)
- [AWS S3 + CloudFront](https://docs.aws.amazon.com/AmazonS3/latest/dev/HostingWebsiteOnS3Setup.html)

---

## 📋 Deployment Checklist

```
Pre-Deployment:
- [ ] All tests pass
- [ ] No console errors
- [ ] API URL configured for production
- [ ] Backend deployed and accessible
- [ ] SSL certificate ready

Deployment:
- [ ] Build succeeds locally
- [ ] Preview works locally
- [ ] Deployment platform configured
- [ ] Environment variables set
- [ ] Deploy successful

Post-Deployment:
- [ ] App loads and runs
- [ ] All features work
- [ ] No console errors
- [ ] Performance acceptable
- [ ] Security headers present
- [ ] Monitoring enabled

Maintenance:
- [ ] Regular backups
- [ ] Security updates
- [ ] Performance monitoring
- [ ] Error tracking
- [ ] User feedback collection
```

---

**Happy Deploying!** 🚀

Your MNP Frontend is ready for production!
