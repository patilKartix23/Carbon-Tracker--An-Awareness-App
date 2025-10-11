# 🚀 Complete Deployment Guide - Carbon Tracker App

This guide will walk you through deploying your Climate Tracker app to the internet **for FREE**!

## 📋 What You'll Need

1. ✅ GitHub account (you already have this!)
2. ✅ Vercel account (for frontend - we'll create this)
3. ✅ Render account (for backend - we'll create this)

---

## 🎯 STEP 1: Prepare Your Application

### A. Update Frontend to Connect to Deployed Backend

We'll do this together after you get your backend URL from Render.

---

## 🔧 STEP 2: Deploy Backend to Render (FREE)

### 2.1 Create Render Account

1. **Go to**: https://render.com
2. Click **"Get Started for Free"**
3. Sign up with your **GitHub account** (easiest option)
4. Authorize Render to access your GitHub

### 2.2 Create Web Service

1. Once logged in, click **"New +"** button (top right)
2. Select **"Web Service"**
3. Connect your GitHub repository:
   - Click **"Connect account"** if not connected
   - Find and select: `Carbon-Tracker--An-Awareness-App`
   - Click **"Connect"**

### 2.3 Configure Backend Service

Fill in these settings:

| Setting | Value |
|---------|-------|
| **Name** | `carbon-tracker-backend` (or any name you like) |
| **Region** | Choose closest to you (e.g., Oregon USA) |
| **Branch** | `main` |
| **Root Directory** | `backend` |
| **Runtime** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `gunicorn app:app --bind 0.0.0.0:$PORT` |

### 2.4 Add Environment Variables

Scroll down to **"Environment Variables"** section and add:

```
SECRET_KEY=your_secret_key_change_this_in_production
GEMINI_API_KEY=your_gemini_api_key_here
DATABASE_URL=sqlite:///./climate_tracker.db
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
DEBUG=False
```

### 2.5 Choose Free Plan

1. Scroll down to **"Instance Type"**
2. Select **"Free"** (Includes 750 hours/month - enough for your app!)
3. Click **"Create Web Service"**

### 2.6 Wait for Deployment

- Render will start building your backend
- This takes 5-10 minutes
- You'll see logs in real-time
- Once done, you'll get a URL like: `https://carbon-tracker-backend.onrender.com`

**⚠️ IMPORTANT: Copy this URL! You'll need it for the frontend.**

---

## 🎨 STEP 3: Deploy Frontend to Vercel (FREE)

### 3.1 Create Vercel Account

1. **Go to**: https://vercel.com
2. Click **"Sign Up"**
3. Choose **"Continue with GitHub"**
4. Authorize Vercel to access your GitHub

### 3.2 Import Your Project

1. Click **"Add New..."** → **"Project"**
2. Find `Carbon-Tracker--An-Awareness-App` in the list
3. Click **"Import"**

### 3.3 Configure Frontend Deployment

| Setting | Value |
|---------|-------|
| **Framework Preset** | Vite |
| **Root Directory** | `frontend` (click "Edit" to change) |
| **Build Command** | `npm run build` |
| **Output Directory** | `dist` |

### 3.4 Add Environment Variable

Click **"Environment Variables"** and add:

```
VITE_API_URL=https://carbon-tracker-backend.onrender.com
```

⚠️ **Replace** `https://carbon-tracker-backend.onrender.com` with YOUR actual Render backend URL!

### 3.5 Deploy!

1. Click **"Deploy"**
2. Wait 2-3 minutes
3. Vercel will give you a URL like: `https://carbon-tracker.vercel.app`

---

## ✅ STEP 4: Test Your Deployed App

1. Open your Vercel URL in a browser
2. Try logging in with the demo user
3. Test different features:
   - Carbon tracking
   - Social feed
   - EcoMarket
   - AI Chatbot

---

## 🔧 STEP 5: Connect Frontend to Backend (IMPORTANT!)

We need to update your frontend code to use the deployed backend URL instead of localhost.

### Create a Production API Client

I'll help you do this in the next steps!

---

## 🐛 Troubleshooting

### Backend Issues:

**Problem**: Build fails
- **Solution**: Check if `requirements.txt` is correct
- **Solution**: Make sure `gunicorn` is in requirements.txt

**Problem**: Backend keeps sleeping (Render free tier)
- **Solution**: Free tier sleeps after 15 min inactivity - this is normal
- **Solution**: First request after sleep takes 30-60 seconds to wake up

### Frontend Issues:

**Problem**: Can't connect to backend
- **Solution**: Check CORS settings in backend
- **Solution**: Verify VITE_API_URL is correct

**Problem**: Environment variables not working
- **Solution**: In Vercel, redeploy after adding env vars

---

## 📱 STEP 6: Custom Domain (Optional)

### For Vercel (Frontend):
1. Go to your project settings
2. Click "Domains"
3. Add your custom domain
4. Follow DNS instructions

### For Render (Backend):
1. Free tier doesn't support custom domains
2. Upgrade to paid plan ($7/month) for custom domains

---

## 💰 Cost Breakdown

| Service | Free Tier | Limits |
|---------|-----------|--------|
| **Vercel** | ✅ Free | 100GB bandwidth, unlimited sites |
| **Render** | ✅ Free | 750 hours/month, sleeps after 15min inactivity |
| **GitHub** | ✅ Free | Unlimited public repos |

**Total Monthly Cost: $0** 🎉

---

## 🔄 How to Update Your Deployed App

Whenever you make changes to your code:

```bash
# Make your changes, then:
git add .
git commit -m "Description of changes"
git push
```

- **Vercel**: Automatically redeploys on push (1-2 minutes)
- **Render**: Automatically redeploys on push (5-10 minutes)

---

## 🎓 Next Steps

1. **Monitor Performance**: Both Render and Vercel have dashboards to monitor your app
2. **Add Analytics**: Consider Google Analytics or Vercel Analytics
3. **SSL/HTTPS**: Both platforms provide free SSL certificates automatically
4. **Database**: For production, consider upgrading to PostgreSQL on Render

---

## 📞 Need Help?

- **Vercel Docs**: https://vercel.com/docs
- **Render Docs**: https://render.com/docs
- **Your GitHub Issues**: Open issues in your repo for community help

---

**Ready to deploy? Let's start with Step 2! 🚀**
