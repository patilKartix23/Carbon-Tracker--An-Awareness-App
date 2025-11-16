"""
Firebase Service for CarbonSense App
Handles all Firestore operations for the application
"""
from typing import Dict, List, Optional, Any
from datetime import datetime
from firebase_admin import firestore
from database.connection import get_firestore
import structlog

logger = structlog.get_logger()


class FirebaseService:
    """Service class for Firebase Firestore operations"""
    
    def __init__(self):
        self.db = get_firestore()
    
    # ================== USER MANAGEMENT ==================
    
    async def create_user_profile(self, user_id: str, user_data: Dict) -> bool:
        """Create or update user profile in Firestore"""
        try:
            if not self.db:
                logger.warning("Firebase not available")
                return False
            
            user_ref = self.db.collection('users').document(user_id)
            user_ref.set({
                **user_data,
                'created_at': firestore.SERVER_TIMESTAMP,
                'updated_at': firestore.SERVER_TIMESTAMP
            }, merge=True)
            
            logger.info("User profile created", user_id=user_id)
            return True
        except Exception as e:
            logger.error("Error creating user profile", error=str(e))
            return False
    
    async def get_user_profile(self, user_id: str) -> Optional[Dict]:
        """Get user profile from Firestore"""
        try:
            if not self.db:
                return None
            
            doc = self.db.collection('users').document(user_id).get()
            if doc.exists:
                return doc.to_dict()
            return None
        except Exception as e:
            logger.error("Error getting user profile", error=str(e))
            return None
    
    async def update_user_stats(self, user_id: str, stats: Dict) -> bool:
        """Update user statistics (carbon saved, points, etc.)"""
        try:
            if not self.db:
                return False
            
            user_ref = self.db.collection('users').document(user_id)
            user_ref.update({
                'stats': stats,
                'updated_at': firestore.SERVER_TIMESTAMP
            })
            return True
        except Exception as e:
            logger.error("Error updating user stats", error=str(e))
            return False
    
    # ================== CARBON TRACKING ==================
    
    async def log_carbon_activity(self, user_id: str, activity: Dict) -> str:
        """Log a carbon footprint activity"""
        try:
            if not self.db:
                return ""
            
            activity_data = {
                **activity,
                'user_id': user_id,
                'timestamp': firestore.SERVER_TIMESTAMP,
                'status': 'completed'
            }
            
            # Add to user's activities subcollection
            doc_ref = self.db.collection('users').document(user_id).collection('carbon_activities').add(activity_data)
            
            # Also add to global activities for analytics
            self.db.collection('carbon_logs').add(activity_data)
            
            logger.info("Carbon activity logged", user_id=user_id, activity_type=activity.get('type'))
            return doc_ref[1].id
        except Exception as e:
            logger.error("Error logging carbon activity", error=str(e))
            return ""
    
    async def get_user_carbon_history(self, user_id: str, limit: int = 50) -> List[Dict]:
        """Get user's carbon tracking history"""
        try:
            if not self.db:
                return []
            
            activities = self.db.collection('users').document(user_id).collection('carbon_activities').order_by('timestamp', direction=firestore.Query.DESCENDING).limit(limit).stream()
            
            return [{**doc.to_dict(), 'id': doc.id} for doc in activities]
        except Exception as e:
            logger.error("Error getting carbon history", error=str(e))
            return []
    
    async def get_carbon_analytics(self, user_id: str, period: str = 'month') -> Dict:
        """Get carbon footprint analytics for a period"""
        try:
            if not self.db:
                return {}
            
            # Query activities within time period
            # This is a simplified version - you'd add date filtering
            activities = self.db.collection('users').document(user_id).collection('carbon_activities').stream()
            
            total_emissions = 0
            activities_by_type = {}
            
            for doc in activities:
                data = doc.to_dict()
                emissions = data.get('emissions_kg', 0)
                activity_type = data.get('type', 'unknown')
                
                total_emissions += emissions
                activities_by_type[activity_type] = activities_by_type.get(activity_type, 0) + emissions
            
            return {
                'total_emissions': total_emissions,
                'by_type': activities_by_type,
                'period': period
            }
        except Exception as e:
            logger.error("Error getting carbon analytics", error=str(e))
            return {}
    
    # ================== ADVOCACY & PETITIONS ==================
    
    async def create_petition(self, petition_data: Dict) -> str:
        """Create a new petition"""
        try:
            if not self.db:
                return ""
            
            petition = {
                **petition_data,
                'created_at': firestore.SERVER_TIMESTAMP,
                'signatures_count': 0,
                'status': 'active'
            }
            
            doc_ref = self.db.collection('petitions').add(petition)
            logger.info("Petition created", petition_id=doc_ref[1].id)
            return doc_ref[1].id
        except Exception as e:
            logger.error("Error creating petition", error=str(e))
            return ""
    
    async def sign_petition(self, petition_id: str, user_id: str, signature_data: Dict) -> bool:
        """Sign a petition"""
        try:
            if not self.db:
                return False
            
            # Add signature to signatures subcollection
            self.db.collection('petitions').document(petition_id).collection('signatures').document(user_id).set({
                **signature_data,
                'signed_at': firestore.SERVER_TIMESTAMP
            })
            
            # Increment signature count
            petition_ref = self.db.collection('petitions').document(petition_id)
            petition_ref.update({
                'signatures_count': firestore.Increment(1)
            })
            
            logger.info("Petition signed", petition_id=petition_id, user_id=user_id)
            return True
        except Exception as e:
            logger.error("Error signing petition", error=str(e))
            return False
    
    async def get_petitions(self, category: Optional[str] = None, status: str = 'active', limit: int = 20) -> List[Dict]:
        """Get petitions with optional filtering"""
        try:
            if not self.db:
                return []
            
            query = self.db.collection('petitions').where('status', '==', status)
            
            if category:
                query = query.where('category', '==', category)
            
            query = query.order_by('signatures_count', direction=firestore.Query.DESCENDING).limit(limit)
            
            petitions = query.stream()
            return [{**doc.to_dict(), 'id': doc.id} for doc in petitions]
        except Exception as e:
            logger.error("Error getting petitions", error=str(e))
            return []
    
    # ================== SOCIAL FEED ==================
    
    async def create_post(self, user_id: str, post_data: Dict) -> str:
        """Create a social media post"""
        try:
            if not self.db:
                return ""
            
            post = {
                **post_data,
                'user_id': user_id,
                'created_at': firestore.SERVER_TIMESTAMP,
                'likes_count': 0,
                'comments_count': 0
            }
            
            doc_ref = self.db.collection('posts').add(post)
            logger.info("Post created", post_id=doc_ref[1].id, user_id=user_id)
            return doc_ref[1].id
        except Exception as e:
            logger.error("Error creating post", error=str(e))
            return ""
    
    async def like_post(self, post_id: str, user_id: str) -> bool:
        """Like a post"""
        try:
            if not self.db:
                return False
            
            # Add like to likes subcollection
            self.db.collection('posts').document(post_id).collection('likes').document(user_id).set({
                'liked_at': firestore.SERVER_TIMESTAMP
            })
            
            # Increment like count
            post_ref = self.db.collection('posts').document(post_id)
            post_ref.update({
                'likes_count': firestore.Increment(1)
            })
            
            return True
        except Exception as e:
            logger.error("Error liking post", error=str(e))
            return False
    
    async def add_comment(self, post_id: str, user_id: str, comment_text: str) -> str:
        """Add comment to a post"""
        try:
            if not self.db:
                return ""
            
            comment = {
                'user_id': user_id,
                'text': comment_text,
                'created_at': firestore.SERVER_TIMESTAMP
            }
            
            # Add comment to comments subcollection
            doc_ref = self.db.collection('posts').document(post_id).collection('comments').add(comment)
            
            # Increment comment count
            post_ref = self.db.collection('posts').document(post_id)
            post_ref.update({
                'comments_count': firestore.Increment(1)
            })
            
            return doc_ref[1].id
        except Exception as e:
            logger.error("Error adding comment", error=str(e))
            return ""
    
    async def get_feed(self, user_id: Optional[str] = None, limit: int = 20) -> List[Dict]:
        """Get social feed posts"""
        try:
            if not self.db:
                return []
            
            # Get recent posts
            posts = self.db.collection('posts').order_by('created_at', direction=firestore.Query.DESCENDING).limit(limit).stream()
            
            return [{**doc.to_dict(), 'id': doc.id} for doc in posts]
        except Exception as e:
            logger.error("Error getting feed", error=str(e))
            return []
    
    # ================== LEADERBOARD ==================
    
    async def update_leaderboard(self, user_id: str, points: int, category: str = 'carbon_saved') -> bool:
        """Update user position on leaderboard"""
        try:
            if not self.db:
                return False
            
            leaderboard_ref = self.db.collection('leaderboards').document(category).collection('users').document(user_id)
            
            leaderboard_ref.set({
                'user_id': user_id,
                'points': points,
                'updated_at': firestore.SERVER_TIMESTAMP
            }, merge=True)
            
            return True
        except Exception as e:
            logger.error("Error updating leaderboard", error=str(e))
            return False
    
    async def get_leaderboard(self, category: str = 'carbon_saved', limit: int = 10) -> List[Dict]:
        """Get top users from leaderboard"""
        try:
            if not self.db:
                return []
            
            users = self.db.collection('leaderboards').document(category).collection('users').order_by('points', direction=firestore.Query.DESCENDING).limit(limit).stream()
            
            return [{**doc.to_dict(), 'rank': idx + 1} for idx, doc in enumerate(users)]
        except Exception as e:
            logger.error("Error getting leaderboard", error=str(e))
            return []
    
    # ================== ECO-SHOPPING ==================
    
    async def track_eco_purchase(self, user_id: str, purchase_data: Dict) -> str:
        """Track eco-friendly purchase"""
        try:
            if not self.db:
                return ""
            
            purchase = {
                **purchase_data,
                'user_id': user_id,
                'purchased_at': firestore.SERVER_TIMESTAMP
            }
            
            doc_ref = self.db.collection('users').document(user_id).collection('eco_purchases').add(purchase)
            
            # Update user's eco-score
            user_ref = self.db.collection('users').document(user_id)
            user_ref.update({
                'eco_score': firestore.Increment(purchase_data.get('eco_points', 10))
            })
            
            return doc_ref[1].id
        except Exception as e:
            logger.error("Error tracking purchase", error=str(e))
            return ""
    
    # ================== REAL-TIME LISTENERS ==================
    
    def listen_to_petition_updates(self, petition_id: str, callback):
        """Real-time listener for petition updates"""
        if not self.db:
            return None
        
        def on_snapshot(doc_snapshot, changes, read_time):
            for change in changes:
                if change.type.name == 'MODIFIED':
                    callback(change.document.to_dict())
        
        return self.db.collection('petitions').document(petition_id).on_snapshot(on_snapshot)
    
    # ================== BATCH OPERATIONS ==================
    
    async def batch_create_activities(self, activities: List[Dict]) -> bool:
        """Create multiple activities in a batch"""
        try:
            if not self.db:
                return False
            
            batch = self.db.batch()
            
            for activity in activities:
                doc_ref = self.db.collection('carbon_logs').document()
                batch.set(doc_ref, {
                    **activity,
                    'timestamp': firestore.SERVER_TIMESTAMP
                })
            
            batch.commit()
            logger.info("Batch activities created", count=len(activities))
            return True
        except Exception as e:
            logger.error("Error in batch create", error=str(e))
            return False


# Create global instance
firebase_service = FirebaseService()
