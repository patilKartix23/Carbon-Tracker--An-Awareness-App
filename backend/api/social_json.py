"""
Social Feed API using JSON data (no database required)
Real climate activists from Karnataka
"""
from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from datetime import datetime
import json
from pathlib import Path

router = APIRouter(prefix="/api/v1/social", tags=["social"])

# Load social feed data from JSON
def load_social_data():
    """Load users and posts from JSON file"""
    try:
        json_path = Path(__file__).parent.parent / 'data' / 'social_feed.json'
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            print(f"[Social Feed] Loaded {len(data.get('users', []))} users and {len(data.get('posts', []))} posts with real team photos")
            return data
    except Exception as e:
        print(f"[Social Feed] Error loading: {e}")
        return {"users": [], "posts": [], "comments": []}

SOCIAL_DATA = load_social_data()

@router.get("/posts")
async def get_posts(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    user_id: Optional[str] = None
):
    """Get social feed posts"""
    posts = SOCIAL_DATA.get('posts', []).copy()
    
    # Filter by user if specified
    if user_id:
        posts = [p for p in posts if p.get('author_id') == user_id]
    
    # Sort by created_at (newest first)
    posts.sort(key=lambda x: x.get('created_at', ''), reverse=True)
    
    # Pagination
    paginated_posts = posts[skip:skip + limit]
    
    # Return posts directly as array (frontend expects this format)
    return paginated_posts

@router.get("/posts/{post_id}")
async def get_post(post_id: str):
    """Get single post by ID"""
    post = next((p for p in SOCIAL_DATA.get('posts', []) if p['id'] == post_id), None)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    # Add comments to post
    comments = [c for c in SOCIAL_DATA.get('comments', []) if c.get('post_id') == post_id]
    post_with_comments = post.copy()
    post_with_comments['comments'] = comments
    
    return post_with_comments

@router.post("/posts/{post_id}/like")
async def like_post(post_id: str):
    """Like a post (simulated)"""
    post = next((p for p in SOCIAL_DATA.get('posts', []) if p['id'] == post_id), None)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    # Simulate liking
    post['likes_count'] = post.get('likes_count', 0) + 1
    
    return {
        "success": True,
        "message": "Post liked!",
        "likes_count": post['likes_count']
    }

@router.post("/posts/{post_id}/unlike")
async def unlike_post(post_id: str):
    """Unlike a post (simulated)"""
    post = next((p for p in SOCIAL_DATA.get('posts', []) if p['id'] == post_id), None)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    # Simulate unliking
    post['likes_count'] = max(0, post.get('likes_count', 0) - 1)
    
    return {
        "success": True,
        "message": "Post unliked!",
        "likes_count": post['likes_count']
    }

@router.post("/posts/{post_id}/comments")
async def add_comment(post_id: str, comment_data: dict):
    """Add comment to post (simulated)"""
    post = next((p for p in SOCIAL_DATA.get('posts', []) if p['id'] == post_id), None)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    # Simulate adding comment
    new_comment = {
        "id": f"comment-{len(SOCIAL_DATA.get('comments', [])) + 1}",
        "post_id": post_id,
        "author_id": comment_data.get('author_id', 'anonymous'),
        "author": comment_data.get('author', {"name": "Anonymous", "username": "anonymous"}),
        "content": comment_data.get('content', ''),
        "created_at": datetime.utcnow().isoformat() + 'Z',
        "likes_count": 0
    }
    
    SOCIAL_DATA.get('comments', []).append(new_comment)
    post['comments_count'] = post.get('comments_count', 0) + 1
    
    return {
        "success": True,
        "message": "Comment added!",
        "comment": new_comment
    }

@router.get("/posts/{post_id}/comments")
async def get_comments(post_id: str):
    """Get comments for a post"""
    post = next((p for p in SOCIAL_DATA.get('posts', []) if p['id'] == post_id), None)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    comments = [c for c in SOCIAL_DATA.get('comments', []) if c.get('post_id') == post_id]
    
    # Return comments array directly (frontend expects this format)
    return comments

@router.get("/users")
async def get_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100)
):
    """Get list of users"""
    users = SOCIAL_DATA.get('users', []).copy()
    
    # Sort by followers
    users.sort(key=lambda x: x.get('followers_count', 0), reverse=True)
    
    return {
        "users": users[skip:skip + limit],
        "total": len(users)
    }

@router.get("/users/{user_id}")
async def get_user(user_id: str):
    """Get user profile"""
    user = next((u for u in SOCIAL_DATA.get('users', []) if u['id'] == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Get user's posts
    user_posts = [p for p in SOCIAL_DATA.get('posts', []) if p.get('author_id') == user_id]
    
    user_profile = user.copy()
    user_profile['recent_posts'] = user_posts[:5]  # Last 5 posts
    
    return user_profile

@router.get("/feed/trending")
async def get_trending_posts(limit: int = Query(10, ge=1, le=50)):
    """Get trending posts based on engagement"""
    posts = SOCIAL_DATA.get('posts', []).copy()
    
    # Calculate engagement score
    for post in posts:
        likes = post.get('likes_count', 0)
        comments = post.get('comments_count', 0)
        # More weight to comments as they indicate deeper engagement
        post['engagement_score'] = likes + (comments * 5)
    
    # Sort by engagement
    posts.sort(key=lambda x: x.get('engagement_score', 0), reverse=True)
    
    return {
        "trending_posts": posts[:limit]
    }

@router.get("/stats")
async def get_social_stats():
    """Get overall social platform statistics"""
    users = SOCIAL_DATA.get('users', [])
    posts = SOCIAL_DATA.get('posts', [])
    comments = SOCIAL_DATA.get('comments', [])
    
    total_likes = sum(p.get('likes_count', 0) for p in posts)
    total_trees_planted = sum(u.get('trees_planted', 0) for u in users)
    total_carbon_saved = sum(u.get('carbon_saved_kg', 0) for u in users)
    
    return {
        "total_users": len(users),
        "total_posts": len(posts),
        "total_comments": len(comments),
        "total_likes": total_likes,
        "total_trees_planted": total_trees_planted,
        "total_carbon_saved_kg": total_carbon_saved,
        "active_users_today": len(users)  # Simulated
    }
