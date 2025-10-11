# 🚀 Quick Start Commands - Climate Tracker

## ⚠️ Common Error: npm run dev from wrong directory

### ❌ WRONG (Root directory):
```powershell
cd C:\Users\Admin\Desktop\CLIMATE-APP\climate-tracker-app
npm run dev  # ❌ ERROR: Cannot find package.json
```

### ✅ CORRECT (Frontend directory):
```powershell
cd C:\Users\Admin\Desktop\CLIMATE-APP\climate-tracker-app\frontend
npm run dev  # ✅ Works!
```

---

## 🎯 Quick Start Commands

### Start Both Services (Two Separate Terminals)

#### Terminal 1 - Backend (Flask):
```powershell
cd C:\Users\Admin\Desktop\CLIMATE-APP\climate-tracker-app\backend
$env:FLASK_APP="app.py"
$env:FLASK_RUN_PORT="8000"
python -m flask run --host=0.0.0.0
```

#### Terminal 2 - Frontend (React):
```powershell
cd C:\Users\Admin\Desktop\CLIMATE-APP\climate-tracker-app\frontend
npm run dev
```

---

## 📁 Project Structure

```
climate-tracker-app/
├── backend/              ← Backend Flask app
│   ├── app.py           ← Main Flask file
│   ├── api/             ← API routes
│   └── requirements.txt
│
├── frontend/            ← Frontend React app
│   ├── package.json     ← npm scripts here!
│   ├── src/            ← Source code
│   └── node_modules/
│
└── package.json         ❌ Does NOT exist (root level)
```

---

## 🔑 Key Points

1. **Frontend** has `package.json` → Run `npm` commands from `/frontend`
2. **Backend** has `app.py` → Run Flask commands from `/backend`
3. **Root directory** has NO package.json → Don't run npm commands here

---

## 🌐 Access URLs

Once both servers are running:

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **Social Feed**: http://localhost:3000/social ← Kartik's post is here!
- **Profile Page**: http://localhost:3000/profile

---

## 🛑 Stop Servers

Press `Ctrl+C` in each terminal window to stop the servers.

---

## ✅ Current Status

**Backend**: ✅ Running on http://localhost:8000  
**Frontend**: ✅ Running on http://localhost:3000  
**Kartik's Post**: ✅ Live in Social Feed

---

## 🎯 View Kartik Patil's Post

Navigate to: **http://localhost:3000/social**

You'll see his tree planting post as the **first item** in the feed!

---

**Last Updated**: October 10, 2025  
**Status**: ✅ Both servers running
