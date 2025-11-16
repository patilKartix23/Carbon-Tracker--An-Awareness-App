"""
Firebase API Endpoints for CarbonSense
RESTful API using Firebase Firestore
"""
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from services.firebase_service import firebase_service
import structlog

logger = structlog.get_logger()
router = APIRouter()


# ================== PYDANTIC MODELS ==================

class UserProfile(BaseModel):
    username: str
    email: str
    name: Optional[str] = None
    bio: Optional[str] = None
    location: Optional[str] = None
    carbon_goal: Optional[float] = None


class CarbonActivity(BaseModel):
    type: str  # transport, energy, food, waste
    category: str  # car, bus, electricity, etc.
    amount: float
    unit: str
    emissions_kg: float
    description: Optional[str] = None


class PetitionCreate(BaseModel):
    title: str
    description: str
    category: str
    target_signatures: int
    creator_id: str
    image_url: Optional[str] = None


class SignatureData(BaseModel):
    name: str
    email: Optional[str] = None
    comment: Optional[str] = None


class PostCreate(BaseModel):
    content: str
    image_url: Optional[str] = None
    tags: Optional[List[str]] = []


class CommentCreate(BaseModel):
    text: str


# ================== USER ENDPOINTS ==================

@router.post("/users/{user_id}/profile")
async def create_user_profile(user_id: str, profile: UserProfile):
    """Create or update user profile"""
    success = await firebase_service.create_user_profile(
        user_id, 
        profile.dict()
    )
    
    if success:
        return {"message": "Profile created successfully", "user_id": user_id}
    raise HTTPException(status_code=500, detail="Failed to create profile")


@router.get("/users/{user_id}/profile")
async def get_user_profile(user_id: str):
    """Get user profile"""
    profile = await firebase_service.get_user_profile(user_id)
    
    if profile:
        return profile
    raise HTTPException(status_code=404, detail="User not found")


@router.get("/users/{user_id}/stats")
async def get_user_stats(user_id: str):
    """Get user statistics"""
    profile = await firebase_service.get_user_profile(user_id)
    
    if profile:
        return profile.get('stats', {})
    raise HTTPException(status_code=404, detail="User not found")


# ================== CARBON TRACKING ENDPOINTS ==================

@router.post("/carbon/log/{user_id}")
async def log_carbon_activity(user_id: str, activity: CarbonActivity):
    """Log a carbon footprint activity"""
    activity_id = await firebase_service.log_carbon_activity(
        user_id,
        activity.dict()
    )
    
    if activity_id:
        return {
            "message": "Activity logged successfully",
            "activity_id": activity_id,
            "emissions_kg": activity.emissions_kg
        }
    raise HTTPException(status_code=500, detail="Failed to log activity")


@router.get("/carbon/history/{user_id}")
async def get_carbon_history(user_id: str, limit: int = 50):
    """Get user's carbon tracking history"""
    history = await firebase_service.get_user_carbon_history(user_id, limit)
    
    return {
        "user_id": user_id,
        "activities": history,
        "count": len(history)
    }


@router.get("/carbon/analytics/{user_id}")
async def get_carbon_analytics(user_id: str, period: str = "month"):
    """Get carbon analytics for a period"""
    analytics = await firebase_service.get_carbon_analytics(user_id, period)
    
    return analytics


# ================== ADVOCACY ENDPOINTS ==================

@router.post("/advocacy/petitions")
async def create_petition(petition: PetitionCreate):
    """Create a new petition"""
    petition_id = await firebase_service.create_petition(petition.dict())
    
    if petition_id:
        return {
            "message": "Petition created successfully",
            "petition_id": petition_id
        }
    raise HTTPException(status_code=500, detail="Failed to create petition")


@router.post("/advocacy/petitions/{petition_id}/sign/{user_id}")
async def sign_petition(petition_id: str, user_id: str, signature: SignatureData):
    """Sign a petition"""
    success = await firebase_service.sign_petition(
        petition_id,
        user_id,
        signature.dict()
    )
    
    if success:
        return {"message": "Petition signed successfully"}
    raise HTTPException(status_code=500, detail="Failed to sign petition")


@router.get("/advocacy/petitions")
async def get_petitions(
    category: Optional[str] = None,
    status: str = "active",
    limit: int = 20
):
    """Get petitions with filtering"""
    petitions = await firebase_service.get_petitions(category, status, limit)
    
    return {
        "petitions": petitions,
        "count": len(petitions)
    }


# ================== SOCIAL FEED ENDPOINTS ==================

@router.post("/social/posts/{user_id}")
async def create_post(user_id: str, post: PostCreate):
    """Create a social media post"""
    post_id = await firebase_service.create_post(user_id, post.dict())
    
    if post_id:
        return {
            "message": "Post created successfully",
            "post_id": post_id
        }
    raise HTTPException(status_code=500, detail="Failed to create post")


@router.post("/social/posts/{post_id}/like/{user_id}")
async def like_post(post_id: str, user_id: str):
    """Like a post"""
    success = await firebase_service.like_post(post_id, user_id)
    
    if success:
        return {"message": "Post liked successfully"}
    raise HTTPException(status_code=500, detail="Failed to like post")


@router.post("/social/posts/{post_id}/comment/{user_id}")
async def add_comment(post_id: str, user_id: str, comment: CommentCreate):
    """Add comment to a post"""
    comment_id = await firebase_service.add_comment(
        post_id,
        user_id,
        comment.text
    )
    
    if comment_id:
        return {
            "message": "Comment added successfully",
            "comment_id": comment_id
        }
    raise HTTPException(status_code=500, detail="Failed to add comment")


@router.get("/social/feed")
async def get_feed(user_id: Optional[str] = None, limit: int = 20):
    """Get social feed"""
    posts = await firebase_service.get_feed(user_id, limit)
    
    return {
        "posts": posts,
        "count": len(posts)
    }


# ================== LEADERBOARD ENDPOINTS ==================

@router.get("/leaderboard/{category}")
async def get_leaderboard(category: str = "carbon_saved", limit: int = 10):
    """Get leaderboard rankings"""
    rankings = await firebase_service.get_leaderboard(category, limit)
    
    return {
        "category": category,
        "rankings": rankings,
        "count": len(rankings)
    }


@router.post("/leaderboard/{category}/update/{user_id}")
async def update_leaderboard(category: str, user_id: str, points: int):
    """Update user's leaderboard position"""
    success = await firebase_service.update_leaderboard(user_id, points, category)
    
    if success:
        return {"message": "Leaderboard updated successfully"}
    raise HTTPException(status_code=500, detail="Failed to update leaderboard")


# ================== ECO-SHOPPING ENDPOINTS ==================

class EcoPurchase(BaseModel):
    product_id: str
    product_name: str
    carbon_saved: float
    eco_points: int
    price: float


@router.post("/eco-shopping/purchase/{user_id}")
async def track_purchase(user_id: str, purchase: EcoPurchase):
    """Track eco-friendly purchase"""
    purchase_id = await firebase_service.track_eco_purchase(
        user_id,
        purchase.dict()
    )
    
    if purchase_id:
        return {
            "message": "Purchase tracked successfully",
            "purchase_id": purchase_id,
            "eco_points_earned": purchase.eco_points
        }
    raise HTTPException(status_code=500, detail="Failed to track purchase")
