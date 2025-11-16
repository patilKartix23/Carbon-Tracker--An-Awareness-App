# Complete Firebase Backend Utilization Guide

## 🚀 What You Can Do With Firebase

Your CarbonSense app now has a **full-featured Firebase backend** with these capabilities:

### ✅ **Features Implemented:**

1. **User Profiles & Management**
2. **Carbon Tracking & Analytics**
3. **Advocacy & Petitions**
4. **Social Feed (Posts, Likes, Comments)**
5. **Leaderboards**
6. **Eco-Shopping Tracking**
7. **Real-time Updates**
8. **Batch Operations**

---

## 📚 API Documentation

### Base URL
```
http://localhost:8000/api/v1/firebase
```

---

## 1️⃣ User Management

### Create/Update User Profile
```bash
POST /api/v1/firebase/users/{user_id}/profile

Body:
{
  "username": "kartik_climate",
  "email": "kartik@example.com",
  "name": "Kartik Patil",
  "bio": "Climate activist fighting for a sustainable future",
  "location": "Mumbai, India",
  "carbon_goal": 1000.0
}
```

### Get User Profile
```bash
GET /api/v1/firebase/users/{user_id}/profile
```

### Get User Stats
```bash
GET /api/v1/firebase/users/{user_id}/stats
```

---

## 2️⃣ Carbon Tracking

### Log Carbon Activity
```bash
POST /api/v1/firebase/carbon/log/{user_id}

Body:
{
  "type": "transport",
  "category": "car",
  "amount": 25.5,
  "unit": "km",
  "emissions_kg": 4.9,
  "description": "Drive to work"
}
```

### Get Carbon History
```bash
GET /api/v1/firebase/carbon/history/{user_id}?limit=50
```

### Get Carbon Analytics
```bash
GET /api/v1/firebase/carbon/analytics/{user_id}?period=month
```

**Response:**
```json
{
  "total_emissions": 145.5,
  "by_type": {
    "transport": 98.2,
    "energy": 32.1,
    "food": 15.2
  },
  "period": "month"
}
```

---

## 3️⃣ Advocacy & Petitions

### Create Petition
```bash
POST /api/v1/firebase/advocacy/petitions

Body:
{
  "title": "Ban Single-Use Plastics in Mumbai",
  "description": "Reduce plastic pollution in our oceans",
  "category": "waste",
  "target_signatures": 10000,
  "creator_id": "user123",
  "image_url": "https://example.com/image.jpg"
}
```

### Sign Petition
```bash
POST /api/v1/firebase/advocacy/petitions/{petition_id}/sign/{user_id}

Body:
{
  "name": "Kartik Patil",
  "email": "kartik@example.com",
  "comment": "I fully support this cause!"
}
```

### Get Petitions
```bash
GET /api/v1/firebase/advocacy/petitions?category=waste&status=active&limit=20
```

---

## 4️⃣ Social Feed

### Create Post
```bash
POST /api/v1/firebase/social/posts/{user_id}

Body:
{
  "content": "Just reduced my carbon footprint by 30% this month! 🌱",
  "image_url": "https://example.com/achievement.jpg",
  "tags": ["carbon", "achievement"]
}
```

### Like Post
```bash
POST /api/v1/firebase/social/posts/{post_id}/like/{user_id}
```

### Add Comment
```bash
POST /api/v1/firebase/social/posts/{post_id}/comment/{user_id}

Body:
{
  "text": "Amazing work! Keep it up!"
}
```

### Get Feed
```bash
GET /api/v1/firebase/social/feed?limit=20
```

---

## 5️⃣ Leaderboards

### Get Leaderboard
```bash
GET /api/v1/firebase/leaderboard/carbon_saved?limit=10
```

**Response:**
```json
{
  "category": "carbon_saved",
  "rankings": [
    {
      "user_id": "user123",
      "points": 500,
      "rank": 1
    },
    {
      "user_id": "user456",
      "points": 450,
      "rank": 2
    }
  ]
}
```

### Update Leaderboard
```bash
POST /api/v1/firebase/leaderboard/carbon_saved/update/{user_id}?points=550
```

---

## 6️⃣ Eco-Shopping

### Track Purchase
```bash
POST /api/v1/firebase/eco-shopping/purchase/{user_id}

Body:
{
  "product_id": "prod123",
  "product_name": "Bamboo Toothbrush",
  "carbon_saved": 0.5,
  "eco_points": 10,
  "price": 199.0
}
```

---

## 🔥 Testing the APIs

### Using cURL (PowerShell):

```powershell
# Create user profile
curl -X POST http://localhost:8000/api/v1/firebase/users/user123/profile `
  -H "Content-Type: application/json" `
  -d '{
    "username": "kartik_climate",
    "email": "kartik@example.com",
    "name": "Kartik Patil",
    "carbon_goal": 1000.0
  }'

# Log carbon activity
curl -X POST http://localhost:8000/api/v1/firebase/carbon/log/user123 `
  -H "Content-Type: application/json" `
  -d '{
    "type": "transport",
    "category": "car",
    "amount": 25.5,
    "unit": "km",
    "emissions_kg": 4.9
  }'

# Get carbon history
curl http://localhost:8000/api/v1/firebase/carbon/history/user123

# Create petition
curl -X POST http://localhost:8000/api/v1/firebase/advocacy/petitions `
  -H "Content-Type: application/json" `
  -d '{
    "title": "Save the Forests",
    "description": "Protect our green lungs",
    "category": "environment",
    "target_signatures": 5000,
    "creator_id": "user123"
  }'
```

---

## 📱 Frontend Integration (JavaScript/TypeScript)

### Install Firebase SDK:
```bash
cd frontend
npm install firebase
```

### Firebase Config (`src/services/firebase.ts`):

```typescript
import { initializeApp } from 'firebase/app';
import { getFirestore } from 'firebase/firestore';
import { getAuth } from 'firebase/auth';

const firebaseConfig = {
  apiKey: "YOUR_API_KEY",
  authDomain: "carbonsense-48ee2.firebaseapp.com",
  projectId: "carbonsense-48ee2",
  storageBucket: "carbonsense-48ee2.appspot.com",
  messagingSenderId: "YOUR_SENDER_ID",
  appId: "YOUR_APP_ID"
};

const app = initializeApp(firebaseConfig);
export const db = getFirestore(app);
export const auth = getAuth(app);
```

### Usage Example (`src/services/carbonTracking.ts`):

```typescript
import axios from 'axios';

const API_BASE = 'http://localhost:8000/api/v1/firebase';

export const carbonTrackingService = {
  // Log activity
  async logActivity(userId: string, activity: any) {
    const response = await axios.post(
      `${API_BASE}/carbon/log/${userId}`,
      activity
    );
    return response.data;
  },

  // Get history
  async getHistory(userId: string) {
    const response = await axios.get(
      `${API_BASE}/carbon/history/${userId}`
    );
    return response.data;
  },

  // Get analytics
  async getAnalytics(userId: string, period = 'month') {
    const response = await axios.get(
      `${API_BASE}/carbon/analytics/${userId}?period=${period}`
    );
    return response.data;
  }
};
```

### React Component Example:

```typescript
import React, { useState, useEffect } from 'react';
import { carbonTrackingService } from '../services/carbonTracking';

export const CarbonDashboard = () => {
  const [analytics, setAnalytics] = useState(null);
  const userId = 'user123'; // Get from auth

  useEffect(() => {
    loadAnalytics();
  }, []);

  const loadAnalytics = async () => {
    const data = await carbonTrackingService.getAnalytics(userId);
    setAnalytics(data);
  };

  const logActivity = async () => {
    await carbonTrackingService.logActivity(userId, {
      type: 'transport',
      category: 'car',
      amount: 25.5,
      unit: 'km',
      emissions_kg: 4.9
    });
    loadAnalytics(); // Refresh
  };

  return (
    <div>
      <h2>Carbon Analytics</h2>
      {analytics && (
        <div>
          <p>Total Emissions: {analytics.total_emissions} kg CO2</p>
          <button onClick={logActivity}>Log Activity</button>
        </div>
      )}
    </div>
  );
};
```

---

## 🎯 Advanced Features

### Real-time Listeners (Firestore):

```typescript
import { doc, onSnapshot } from 'firebase/firestore';
import { db } from './firebase';

// Listen to petition updates
const petitionRef = doc(db, 'petitions', petitionId);
const unsubscribe = onSnapshot(petitionRef, (doc) => {
  console.log('Petition updated:', doc.data());
});

// Cleanup
unsubscribe();
```

### Batch Operations:

```python
# Backend - batch create activities
from services.firebase_service import firebase_service

activities = [
  {"type": "transport", "emissions_kg": 4.9},
  {"type": "energy", "emissions_kg": 2.1},
  {"type": "food", "emissions_kg": 1.5}
]

await firebase_service.batch_create_activities(activities)
```

---

## 📊 Firestore Data Structure

```
firestore/
├── users/
│   └── {userId}/
│       ├── carbon_activities/
│       ├── eco_purchases/
│       └── (profile fields)
├── petitions/
│   └── {petitionId}/
│       └── signatures/
├── posts/
│   └── {postId}/
│       ├── likes/
│       └── comments/
├── carbon_logs/
└── leaderboards/
    └── {category}/
        └── users/
```

---

## 🔐 Security Best Practices

1. **Set up Firestore Rules** in Firebase Console
2. **Add Authentication** (Firebase Auth)
3. **Validate all inputs** on backend
4. **Rate limiting** for API endpoints
5. **Use environment variables** for sensitive data

---

## 📈 Next Steps

1. ✅ APIs are ready - Test them!
2. ⬜ Add Firebase Auth for user authentication
3. ⬜ Set up Firestore security rules
4. ⬜ Integrate into your React frontend
5. ⬜ Add real-time features
6. ⬜ Deploy to production

---

## 🧪 Quick Test Script

Run this to test all features:

```bash
cd backend
python test_firebase_apis.py
```

(I'll create this script next if you want!)

---

**Your Firebase backend is fully ready to use! 🚀**
