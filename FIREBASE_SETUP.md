# Firebase Integration Guide

## Overview

MongoDB has been removed from the project and replaced with Firebase Firestore for document storage.

## Features

- **Firestore Database**: NoSQL document database for flexible data storage
- **Authentication**: User authentication and authorization
- **Cloud Storage**: File and media storage
- **Real-time Database**: Optional real-time data sync
- **Analytics**: Built-in analytics and monitoring

---

## Setup Instructions

### 1. Create Firebase Project

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Click "Add project"
3. Enter project name (e.g., `carbon-tracker-app`)
4. Enable Google Analytics (optional)
5. Create project

### 2. Enable Firestore Database

1. In Firebase Console, go to **Build** → **Firestore Database**
2. Click "Create database"
3. Start in **test mode** (for development)
4. Choose location (e.g., `us-central1`)
5. Click "Enable"

### 3. Get Service Account Credentials

1. Go to **Project Settings** (gear icon) → **Service accounts**
2. Click "Generate new private key"
3. Download the JSON file
4. Save it as `firebase-credentials.json` in your project root
5. **IMPORTANT**: Add this file to `.gitignore`

### 4. Configure Environment Variables

Add to your `.env` file:

```env
# Firebase Configuration
FIREBASE_CREDENTIALS_PATH=firebase-credentials.json
FIREBASE_PROJECT_ID=your-project-id
```

### 5. Install Firebase Admin SDK

```bash
cd backend
pip install firebase-admin
```

---

## Usage Examples

### Python Backend (FastAPI)

```python
from database.connection import get_firestore

# Get Firestore client
db = get_firestore()

# Create document
doc_ref = db.collection('users').document('user123')
doc_ref.set({
    'name': 'John Doe',
    'email': 'john@example.com',
    'created_at': firestore.SERVER_TIMESTAMP
})

# Read document
doc = doc_ref.get()
if doc.exists:
    print(doc.to_dict())

# Query collection
users = db.collection('users').where('age', '>=', 18).stream()
for user in users:
    print(user.to_dict())

# Update document
doc_ref.update({
    'last_login': firestore.SERVER_TIMESTAMP
})

# Delete document
doc_ref.delete()
```

### Frontend (JavaScript)

1. **Install Firebase SDK:**

```bash
cd frontend
npm install firebase
```

2. **Initialize Firebase:**

```javascript
// src/services/firebase.ts
import { initializeApp } from 'firebase/app';
import { getFirestore } from 'firebase/firestore';
import { getAuth } from 'firebase/auth';

const firebaseConfig = {
  apiKey: import.meta.env.VITE_FIREBASE_API_KEY,
  authDomain: import.meta.env.VITE_FIREBASE_AUTH_DOMAIN,
  projectId: import.meta.env.VITE_FIREBASE_PROJECT_ID,
  storageBucket: import.meta.env.VITE_FIREBASE_STORAGE_BUCKET,
  messagingSenderId: import.meta.env.VITE_FIREBASE_MESSAGING_SENDER_ID,
  appId: import.meta.env.VITE_FIREBASE_APP_ID
};

const app = initializeApp(firebaseConfig);
export const db = getFirestore(app);
export const auth = getAuth(app);
```

3. **Use Firestore:**

```javascript
import { collection, addDoc, getDocs, query, where } from 'firebase/firestore';
import { db } from './firebase';

// Add document
const docRef = await addDoc(collection(db, 'activities'), {
  type: 'carbon_tracking',
  amount: 25.5,
  timestamp: new Date()
});

// Get documents
const q = query(collection(db, 'activities'), where('type', '==', 'carbon_tracking'));
const querySnapshot = await getDocs(q);
querySnapshot.forEach((doc) => {
  console.log(doc.id, ' => ', doc.data());
});
```

---

## Security Rules

Set up Firestore security rules in Firebase Console:

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // Allow authenticated users to read/write their own data
    match /users/{userId} {
      allow read, write: if request.auth != null && request.auth.uid == userId;
    }
    
    // Public read for certain collections
    match /advocacy/{document=**} {
      allow read: if true;
      allow write: if request.auth != null;
    }
    
    // Admin only for system data
    match /system/{document=**} {
      allow read, write: if request.auth != null && 
                            get(/databases/$(database)/documents/users/$(request.auth.uid)).data.role == 'admin';
    }
  }
}
```

---

## Frontend Environment Variables

Add to `frontend/.env`:

```env
VITE_FIREBASE_API_KEY=your-api-key
VITE_FIREBASE_AUTH_DOMAIN=your-app.firebaseapp.com
VITE_FIREBASE_PROJECT_ID=your-project-id
VITE_FIREBASE_STORAGE_BUCKET=your-app.appspot.com
VITE_FIREBASE_MESSAGING_SENDER_ID=your-sender-id
VITE_FIREBASE_APP_ID=your-app-id
```

Get these values from **Project Settings** → **General** → **Your apps**

---

## Data Migration

If you have existing data, create a migration script:

```python
# backend/scripts/migrate_to_firebase.py
import asyncio
from database.connection import get_firestore, get_db
from models.user import User

async def migrate_users():
    db = next(get_db())
    firestore_db = get_firestore()
    
    if not firestore_db:
        print("Firebase not configured")
        return
    
    users = db.query(User).all()
    
    for user in users:
        firestore_db.collection('users').document(str(user.id)).set({
            'username': user.username,
            'email': user.email,
            'created_at': user.created_at,
            'updated_at': user.updated_at
        })
        print(f"Migrated user: {user.username}")

if __name__ == "__main__":
    asyncio.run(migrate_users())
```

---

## Best Practices

1. **Structure your data**: Plan collections and documents carefully
2. **Use subcollections**: For nested data (e.g., `users/{userId}/activities/{activityId}`)
3. **Optimize queries**: Create indexes for frequently queried fields
4. **Batch operations**: Use batch writes for multiple operations
5. **Security**: Always validate data on the server side
6. **Cost optimization**: 
   - Cache frequently accessed data
   - Use Cloud Functions for server-side logic
   - Minimize document reads/writes

---

## Common Collections Structure

```
firestore/
├── users/
│   └── {userId}/
│       ├── profile/
│       ├── activities/
│       └── settings/
├── advocacy/
│   ├── petitions/
│   └── stories/
├── carbon_logs/
├── products/
└── analytics/
```

---

## Troubleshooting

### Firebase not connecting

1. Check credentials file path in `.env`
2. Verify service account has Firestore permissions
3. Check project ID matches

### Permission denied

1. Review Firestore security rules
2. Ensure user is authenticated
3. Check document paths

### Slow queries

1. Create composite indexes in Firebase Console
2. Limit query results
3. Use pagination

---

## Resources

- [Firebase Documentation](https://firebase.google.com/docs)
- [Firestore Guides](https://firebase.google.com/docs/firestore)
- [Security Rules](https://firebase.google.com/docs/firestore/security/get-started)
- [Python Admin SDK](https://firebase.google.com/docs/admin/setup)
- [JavaScript SDK](https://firebase.google.com/docs/web/setup)

---

## Next Steps

1. ✅ Remove MongoDB dependencies
2. ✅ Add Firebase Admin SDK
3. ⬜ Set up Firebase project
4. ⬜ Configure environment variables
5. ⬜ Update API endpoints to use Firestore
6. ⬜ Add Firebase to frontend
7. ⬜ Migrate existing data (if any)
8. ⬜ Set up security rules
9. ⬜ Test integration
10. ⬜ Deploy to production
