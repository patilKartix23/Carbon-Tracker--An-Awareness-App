"""
Test Firebase Firestore Connection
Run this to verify Firebase is properly integrated
"""
import asyncio
from database.connection import init_db, get_firestore
from datetime import datetime

async def test_firebase():
    print("🔄 Initializing database connections...")
    await init_db()
    
    db = get_firestore()
    
    if db:
        print("✅ Firebase Firestore connected!")
        
        # Test write
        print("\n📝 Testing write operation...")
        test_collection = db.collection('test_connection')
        doc_ref = test_collection.document('test_doc')
        doc_ref.set({
            'message': 'Hello from CarbonSense!',
            'timestamp': datetime.now(),
            'status': 'connected'
        })
        print("✅ Write successful!")
        
        # Test read
        print("\n📖 Testing read operation...")
        doc = doc_ref.get()
        if doc.exists:
            print(f"✅ Read successful! Data: {doc.to_dict()}")
        
        # Clean up
        print("\n🗑️  Cleaning up test data...")
        doc_ref.delete()
        print("✅ Test completed successfully!")
        
    else:
        print("❌ Firebase not configured or credentials missing")
        print("Make sure firebase-credentials.json exists and FIREBASE_CREDENTIALS_PATH is set in .env")

if __name__ == "__main__":
    asyncio.run(test_firebase())
