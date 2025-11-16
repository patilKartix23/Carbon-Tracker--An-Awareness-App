# Netlify Deployment Guide for CarbonSense

## 🚀 Quick Deploy with Backend Integration

### Option 1: Manual Deployment (Current Method)

1. **Build the frontend:**
   ```bash
   cd frontend
   npm run build
   ```

2. **Copy netlify.toml to dist:**
   ```bash
   Copy-Item netlify.toml dist/netlify.toml
   ```

3. **Deploy:**
   - Go to: https://app.netlify.com/projects/carbonsense-web
   - Drag the `frontend/dist` folder to "Deploy manually"
   - ✅ Done! Backend will automatically proxy to Render

### Option 2: Connect to Git (Recommended for Auto-Deploy)

1. **In Netlify Dashboard:**
   - Click "**Connect to Git**"
   - Select your GitHub repository
   - Configure build settings:
     ```
     Base directory: frontend
     Build command: npm run build
     Publish directory: frontend/dist
     ```

2. **The `netlify.toml` will automatically:**
   - Proxy `/api/*` requests to your Render backend
   - Handle React Router SPA routing
   - Add security headers

### 🔧 Backend Configuration

Your backend is already deployed on Render:
- **URL:** https://carbon-tracker-an-awareness-app.onrender.com
- **Proxy configured in:** `netlify.toml`

All API calls from frontend (`/api/*`) will automatically redirect to Render backend.

### ✅ What's Configured

The `netlify.toml` file handles:
- ✅ API proxy to Render backend
- ✅ SPA routing (React Router support)
- ✅ CORS headers
- ✅ Security headers
- ✅ Build settings

### 🧪 Testing After Deployment

1. Open your Netlify URL: https://carbonsense-web.netlify.app
2. Test API calls - they should work automatically
3. Check browser console for any CORS errors (should be none)

### 📝 Environment Variables (Optional)

If you want to override the backend URL:

**Netlify Dashboard → Site Settings → Environment Variables:**
```
VITE_API_URL = https://carbon-tracker-an-awareness-app.onrender.com
```

Then rebuild the site.

---

## 🎉 You're All Set!

Your frontend will now communicate with your backend on Render seamlessly.
