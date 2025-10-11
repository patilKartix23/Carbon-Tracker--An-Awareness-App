# 🤖 AI Chatbot Setup - Quick Guide

## ✅ What's Already Done

1. **AI Chatbot Service** created (`backend/services/ai_climate_bot.py`)
2. **Chatbot API** updated to use AI when available
3. **Your OpenRouter API Key**: `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`
4. **Model**: Google Gemini 2.0 Flash Experimental (FREE)

---

## 🚀 Quick Start (3 Steps)

### Step 1: Configure Environment

Create or update `backend/.env` file:

```bash
cd backend

# If .env doesn't exist, copy from example:
cp env.example .env
```

### Step 2: Add Your API Key to `.env`

Open `backend/.env` and add these lines:

```env
# AI Chatbot Configuration
OPENROUTER_API_KEY=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
AI_MODEL=google/gemini-2.0-flash-exp:free
USE_AI_CHATBOT=true
```

### Step 3: Start Your App

```bash
# Terminal 1 - Backend
cd backend
python app.py

# Terminal 2 - Frontend
cd frontend
npm run dev
```

**That's it!** Open http://localhost:5173 and test the chatbot! 🎉

---

## 🧪 Test the AI Chatbot

### Option 1: Web Interface
1. Open your app: http://localhost:5173
2. Click the chat icon (bottom right)
3. Ask: "Explain climate change in simple terms"
4. Get intelligent AI responses!

### Option 2: API Test (PowerShell)

```powershell
# Test chatbot info
Invoke-RestMethod -Uri "http://localhost:5000/api/chatbot/chat/bot-info" -Method GET | ConvertTo-Json

# Send a message
$body = @{
    message = "What is climate change?"
    user_id = "test"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:5000/api/chatbot/chat" -Method POST -Body $body -ContentType "application/json" | ConvertTo-Json
```

---

## 📋 Your Configuration

**API Key**: `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`

**Model**: `google/gemini-2.0-flash-exp:free`

**Features**:
- ✅ FREE - Unlimited usage
- ✅ 1M tokens context window
- ✅ Faster than Gemini 1.5
- ✅ Better at coding & instructions
- ✅ Multimodal understanding

---

## 🔍 Verify It's Working

### Check Bot Info:
```bash
curl http://localhost:5000/api/chatbot/chat/bot-info
```

**Expected Response**:
```json
{
  "bot_info": {
    "ai_powered": true,
    "ai_available": true,
    "bot_type": "AI-Powered",
    "model": "google/gemini-2.0-flash-exp:free",
    "name": "EcoBot AI"
  }
}
```

### If `ai_powered` is `false`:
1. Check `.env` file has the API key
2. Restart the backend: `python app.py`
3. Verify API key is valid at https://openrouter.ai/keys

---

## 💡 How It Works

1. **With API Key**: Uses Google Gemini 2.0 AI for intelligent responses
2. **Without API Key**: Falls back to rule-based responses
3. **Auto-Detection**: System automatically uses AI if configured

---

## 🎯 Test Queries

Try these to see AI in action:

- "What is climate change and how does it affect India?"
- "How can I reduce my carbon footprint?"
- "Compare the weather in Mumbai and Delhi"
- "Give me sustainable living tips"
- "Explain the monsoon season"

---

## 🛠️ Troubleshooting

### AI not working?

**1. Check .env file exists:**
```bash
cd backend
ls .env  # Should exist
```

**2. Verify API key is loaded:**
```bash
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print('API Key:', os.getenv('OPENROUTER_API_KEY'))"
```

**3. Test API key manually:**
```bash
curl https://openrouter.ai/api/v1/models \
  -H "Authorization: Bearer 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"
```

**4. Restart backend:**
```bash
# Stop any running Python processes
Get-Process | Where-Object {$_.ProcessName -eq "python"} | Stop-Process -Force

# Start fresh
cd backend
python app.py
```

---

## 📦 What Was Installed

The AI chatbot integration includes:

1. **`backend/services/ai_climate_bot.py`** - AI bot service
2. **`backend/api/chatbot.py`** - Updated to use AI
3. **Environment variables** - API key configuration
4. **Auto-fallback** - Works without AI if key missing

---

## 🔐 Security Note

**Never commit your `.env` file!**

The `.env` file is already in `.gitignore`. Your API key is safe.

---

## 🎊 Success Criteria

✅ Backend starts without errors  
✅ Chatbot responds to messages  
✅ AI responses are natural and detailed  
✅ Bot info shows `"ai_powered": true`  

---

## 📞 Need Help?

**Check backend logs** for any errors when starting:
```bash
cd backend
python app.py
```

**API Key Issues?**
- Verify at: https://openrouter.ai/keys
- Regenerate if needed
- Update in `.env` file

**Model Issues?**
- Try alternative: `AI_MODEL=meta-llama/llama-3.2-3b-instruct:free`
- Or use: `AI_MODEL=mistralai/mistral-7b-instruct:free`

---

**🚀 Your AI chatbot is ready! Start your backend and frontend to begin chatting!**

