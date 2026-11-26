# MNP Frontend - Production Deployment Guide

Guide for building and hosting the MNP Frontend in production environments.

---

## 🏗️ Building for Production

Ensure dependencies are installed and execute the production build:

```bash
cd mnp-frontend
npm ci
npm run build
```

This compiles TypeScript and produces optimized static assets in `dist/`:
- Bundled and minified HTML, CSS, and JS (~75KB gzipped)
- Static assets and SVG icons
- Cache-busted asset hashing

Test the production bundle locally:
```bash
npm run preview
```

---

## ☁️ Deployment Targets

### 1. Nginx / Docker Container (Self-Hosted)

Example `Dockerfile`:
```dockerfile
# Build stage
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Production serve stage
FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

`nginx.conf` (SPA fallback):
```nginx
server {
    listen 80;
    server_name localhost;

    location / {
        root /usr/share/nginx/html;
        index index.html;
        try_files $uri $uri/ /index.html;
    }
}
```

### 2. Vercel

```bash
npm install -g vercel
vercel
```
Set environment variable in Vercel project settings:
- `VITE_API_URL`: `https://your-backend-api-domain.com`

### 3. Netlify

Create `netlify.toml`:
```toml
[build]
  publish = "dist"
  command = "npm run build"

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
```
Set `VITE_API_URL` in Netlify dashboard settings.
