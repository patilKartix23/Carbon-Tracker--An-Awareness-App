# Complete Deployment Guide - CarbonSense App

## 🎯 Overview

This guide covers deploying both:
1. **Backend (FastAPI)** → Render
2. **Frontend (React/Vite)** → Netlify

---

## 1️⃣ Deploy Backend to Render

### Step 1: Prepare Firebase Credentials

Your backend needs the Firebase service account JSON file in production.

**Option A: Upload via Render Dashboard (Recommended)**

1. Go to your Render service: https://dashboard.render.com/web/srv-cte67j5umphs73bqc8ig
2. Go to **Environment** tab
3. Add **Secret File**:
   - **Filename**: `firebase-credentials.json`
   - **Contents**: Paste the entire contents of your local `firebase-credentials.json`

**Option B: Use Environment Variable**

Alternatively, you can set the entire JSON as an environment variable:
```
FIREBASE_CREDENTIALS_JSON={"type":"service_account","project_id":"carbonsense-48ee2",...}
```

Then update `backend/database/connection.py` to read from env var if file doesn't exist.

### Step 2: Set Environment Variables on Render

Go to **Environment** tab and add these variables:

```env
# Application
ENVIRONMENT=production
DEBUG=False
SECRET_KEY=<generate-a-secure-random-key>
HOST=0.0.0.0
PORT=8000

# Firebase
FIREBASE_CREDENTIALS_PATH=firebase-credentials.json
FIREBASE_PROJECT_ID=carbonsense-48ee2

# CORS - Add your Netlify domain
ALLOWED_ORIGINS=["https://carbonsense-web.netlify.app","http://localhost:3000"]

# API Keys
OPENWEATHER_API_KEY=<your-api-key>

# Optional
POSTGRES_HOST=
REDIS_URL=
```

### Step 3: Deploy Backend

Since your backend is already connected to GitHub:

1. **Trigger Deploy**:
   - Go to Render Dashboard
   - Click **"Manual Deploy"** → **"Deploy latest commit"**
   - OR: It will auto-deploy on next git push

2. **Monitor Logs**:
   - Watch the build logs for any errors
   - Look for: "✅ Firebase Firestore connected!" message

3. **Verify Backend**:
   ```bash
   # Test health endpoint
   curl https://carbon-tracker-an-awareness-app.onrender.com/health
   
   # Test API docs
   # Open: https://carbon-tracker-an-awareness-app.onrender.com/docs
   ```

### Step 4: Test Firebase Connection on Render

After deployment, check logs for:
```
INFO: Connected to Firebase Firestore
INFO: Application startup complete
```

If you see warnings about Firebase, verify the credentials file was uploaded correctly.

---

## 2️⃣ Deploy Frontend to Netlify

### Method 1: Manual Drag & Drop (Quick)

✅ **Your build is already ready!**

1. **Go to Netlify**:
   - Site: https://app.netlify.com/sites/carbonsense-web

2. **Deploy**:
   - Drag the entire `frontend/dist` folder to the deploy drop zone
   - Wait for deployment to complete (~30 seconds)

3. **Verify**:
   - Visit: https://carbonsense-web.netlify.app
   - Check that API calls work (they should proxy to Render)

### Method 2: Connect to GitHub (Auto-Deploy)

For automatic deployments on every push:

1. **In Netlify Dashboard**:
   - Click **"Set up a new site from Git"** or **"Import from Git"**
   - Select **GitHub**
   - Choose repository: `patilKartix23/Carbon-Tracker--An-Awareness-App`

2. **Configure Build Settings**:
   ```
   Base directory: frontend
   Build command: npm run build
   Publish directory: frontend/dist
   ```

3. **Add Environment Variables** (Optional):
   If you want to override backend URL:
   ```
   VITE_API_URL=https://carbon-tracker-an-awareness-app.onrender.com
   ```

4. **Deploy**:
   - Click **"Deploy site"**
   - Future pushes to `main` branch will auto-deploy

### Frontend Configuration Files

Your frontend already has the correct configuration:

**`frontend/dist/netlify.toml`** ✅
- Proxies `/api/*` to Render backend
- SPA routing configured
- Security headers set

**`frontend/dist/_redirects`** ✅
- Backup redirect rules
- API proxy to Render
- Fallback to index.html

---

## 🧪 Testing Deployed Application

### 1. Test Backend API

```bash
# Health check
curl https://carbon-tracker-an-awareness-app.onrender.com/health

# API documentation
# Open: https://carbon-tracker-an-awareness-app.onrender.com/docs

# Test Firebase endpoints
curl https://carbon-tracker-an-awareness-app.onrender.com/api/v1/firebase/advocacy/petitions
```

### 2. Test Frontend

1. **Visit**: https://carbonsense-web.netlify.app

2. **Test Features**:
   - Homepage loads ✅
   - Navigation works ✅
   - API calls to backend succeed ✅
   - Firebase data loads ✅

3. **Check Browser Console**:
   - No CORS errors (should be clean)
   - API calls go to `/api/*` and proxy to Render

### 3. Test Integration

Create a test petition via frontend:
- Should call: `/api/v1/firebase/advocacy/petitions`
- Should store in Firestore
- Should appear in Firebase Console

---

## 🔥 Firebase Configuration in Production

### Set Up Firestore Security Rules

1. Go to **Firebase Console**: https://console.firebase.google.com
2. Select project: **CarbonSense** (`carbonsense-48ee2`)
3. Go to **Firestore Database** → **Rules**

4. **Set Production Rules**:

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    
    // User profiles - users can only read/write their own
    match /users/{userId} {
      allow read: if request.auth != null;
      allow write: if request.auth != null && request.auth.uid == userId;
      
      // User's carbon activities
      match /carbon_activities/{activity} {
        allow read, write: if request.auth != null && request.auth.uid == userId;
      }
      
      // User's eco purchases
      match /eco_purchases/{purchase} {
        allow read, write: if request.auth != null && request.auth.uid == userId;
      }
    }
    
    // Petitions - public read, authenticated write
    match /petitions/{petition} {
      allow read: if true;  // Public read
      allow create: if request.auth != null;
      allow update, delete: if request.auth != null && 
        resource.data.creator_id == request.auth.uid;
      
      // Petition signatures
      match /signatures/{signature} {
        allow read: if true;
        allow create: if request.auth != null;
      }
    }
    
    // Posts - public read, authenticated write
    match /posts/{post} {
      allow read: if true;
      allow create: if request.auth != null;
      allow update, delete: if request.auth != null && 
        resource.data.user_id == request.auth.uid;
      
      // Post likes and comments
      match /likes/{like} {
        allow read: if true;
        allow create: if request.auth != null;
      }
      
      match /comments/{comment} {
        allow read: if true;
        allow create: if request.auth != null;
        allow delete: if request.auth != null && 
          resource.data.user_id == request.auth.uid;
      }
    }
    
    // Carbon logs - authenticated users only
    match /carbon_logs/{log} {
      allow read: if request.auth != null;
      allow create: if request.auth != null;
    }
    
    // Leaderboards - public read, backend write only
    match /leaderboards/{category}/users/{userId} {
      allow read: if true;
      allow write: if false;  // Only backend can write
    }
  }
}
```

5. **Publish** the rules

**Note**: Currently your backend doesn't use Firebase Auth tokens, so you'll need to either:
- Keep rules permissive for backend service account
- Add Firebase Auth to your app later
- Use admin SDK (which bypasses rules)

Since you're using Firebase Admin SDK in backend, it automatically bypasses security rules. The rules above are for direct client access (if you add Firebase to frontend later).

---

## 🚀 Quick Deploy Commands

### Backend (Render - Auto Deploy)
```bash
# Just push to GitHub
git add .
git commit -m "feat: production updates"
git push origin main

# Render will auto-deploy
```

### Frontend (Netlify - Manual)
```bash
# Build
cd frontend
npm run build

# Copy config
Copy-Item netlify.toml dist/netlify.toml

# Create redirects
echo "/api/*  https://carbon-tracker-an-awareness-app.onrender.com/api/:splat  200
/*      /index.html   200" > dist/_redirects

# Deploy: Drag dist/ folder to Netlify
```

### Frontend (Netlify - Auto Deploy)
```bash
# Just push to GitHub if connected
git push origin main
```

---

## 🔧 Troubleshooting

### Backend Issues

**Problem**: Firebase not connecting
```
Solution:
1. Check Render environment variables
2. Verify FIREBASE_CREDENTIALS_PATH is set correctly
3. Check Secret Files are uploaded
4. Review Render logs for Firebase errors
```

**Problem**: CORS errors from frontend
```
Solution:
1. Add Netlify domain to ALLOWED_ORIGINS
2. Update backend/core/config.py
3. Redeploy backend
```

### Frontend Issues

**Problem**: API calls failing
```
Solution:
1. Check netlify.toml is in dist/
2. Verify _redirects file exists
3. Check Render backend is running
4. Test backend directly: https://carbon-tracker-an-awareness-app.onrender.com/health
```

**Problem**: Routes not working (404 on refresh)
```
Solution:
1. Ensure _redirects has: /* /index.html 200
2. Or netlify.toml has SPA fallback configured
```

---

## 📊 Monitoring Production

### Backend (Render)
- **Logs**: https://dashboard.render.com/web/srv-cte67j5umphs73bqc8ig/logs
- **Metrics**: CPU, Memory, Request count
- **Health**: https://carbon-tracker-an-awareness-app.onrender.com/health

### Frontend (Netlify)
- **Analytics**: Netlify dashboard
- **Deploys**: Deploy history and rollback
- **Functions**: If you add serverless functions later

### Firebase
- **Console**: https://console.firebase.google.com/project/carbonsense-48ee2
- **Firestore Data**: View/edit documents
- **Usage**: Monitor reads/writes (free tier: 50k reads/day)

---

## ✅ Deployment Checklist

### Before Deployment
- [x] Frontend built (`npm run build`)
- [x] netlify.toml in dist/
- [x] _redirects in dist/
- [x] Firebase credentials ready
- [x] Environment variables documented
- [x] Git repository up to date

### Backend Deployment
- [ ] Firebase credentials uploaded to Render
- [ ] Environment variables set on Render
- [ ] Backend deployed successfully
- [ ] Health endpoint returns 200
- [ ] API docs accessible
- [ ] Firebase connection confirmed in logs

### Frontend Deployment
- [ ] Dist folder deployed to Netlify
- [ ] Site loads correctly
- [ ] Navigation works
- [ ] API calls succeed
- [ ] No console errors

### Post-Deployment
- [ ] Test creating petition
- [ ] Test carbon tracking
- [ ] Test social feed
- [ ] Firestore security rules set
- [ ] Monitor Firebase usage
- [ ] Set up error tracking (optional)

---

## 🎉 You're Live!

**Frontend**: https://carbonsense-web.netlify.app  
**Backend**: https://carbon-tracker-an-awareness-app.onrender.com  
**API Docs**: https://carbon-tracker-an-awareness-app.onrender.com/docs

**Firebase Console**: https://console.firebase.google.com/project/carbonsense-48ee2

---

## 📚 Additional Resources

- [Render Documentation](https://render.com/docs)
- [Netlify Documentation](https://docs.netlify.com)
- [Firebase Documentation](https://firebase.google.com/docs)
- [Firestore Security Rules](https://firebase.google.com/docs/firestore/security/get-started)

---

**Need help?** Check the logs or run the TROUBLESHOOT.bat script locally to diagnose issues.
