"""
Social features API routes - Posts, Likes, Comments, Following
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc, func
from typing import List, Optional
import structlog
from datetime import datetime

from database.connection import get_db
from database.models import User, Post, PostLike, PostComment, UserFollow
from api.auth import get_current_active_user
from schemas.social import PostCreate, PostResponse, PostUpdate, CommentCreate, CommentResponse

logger = structlog.get_logger()
router = APIRouter()

@router.post("/posts", response_model=PostResponse)
async def create_post(
    post_data: PostCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Create a new post"""
    try:
        db_post = Post(
            author_id=current_user.id,
            caption=post_data.caption,
            image_url=post_data.image_url,
            latitude=post_data.latitude,
            longitude=post_data.longitude,
            location_name=post_data.location_name,
            weather_data=post_data.weather_data,
            air_quality_data=post_data.air_quality_data,
            is_public=post_data.is_public
        )
        
        db.add(db_post)
        db.commit()
        db.refresh(db_post)
        
        logger.info("Post created", post_id=db_post.id, author_id=current_user.id)
        return db_post
        
    except Exception as e:
        logger.error("Failed to create post", error=str(e))
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create post"
        )

@router.get("/posts", response_model=List[PostResponse])
async def get_posts(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    user_id: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_active_user)
):
    """Get posts feed"""
    try:
        query = db.query(Post).filter(Post.is_public == True)
        
        if user_id:
            query = query.filter(Post.author_id == user_id)
        
        posts = query.order_by(desc(Post.created_at)).offset(skip).limit(limit).all()
        return posts
        
    except Exception as e:
        logger.error("Failed to fetch posts", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch posts"
        )

@router.get("/posts/{post_id}", response_model=PostResponse)
async def get_post(post_id: str, db: Session = Depends(get_db)):
    """Get single post by ID"""
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    return post

@router.put("/posts/{post_id}", response_model=PostResponse)
async def update_post(
    post_id: str,
    post_update: PostUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Update a post"""
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    
    if post.author_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this post"
        )
    
    try:
        update_data = post_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(post, field, value)
        
        post.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(post)
        
        return post
        
    except Exception as e:
        logger.error("Failed to update post", error=str(e))
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update post"
        )

@router.delete("/posts/{post_id}")
async def delete_post(
    post_id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Delete a post"""
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    
    if post.author_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this post"
        )
    
    try:
        db.delete(post)
        db.commit()
        return {"message": "Post deleted successfully"}
        
    except Exception as e:
        logger.error("Failed to delete post", error=str(e))
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete post"
        )

@router.post("/posts/{post_id}/like")
async def toggle_like_post(
    post_id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Like or unlike a post"""
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    
    try:
        existing_like = db.query(PostLike).filter(
            PostLike.post_id == post_id,
            PostLike.user_id == current_user.id
        ).first()
        
        if existing_like:
            # Unlike the post
            db.delete(existing_like)
            post.likes_count = max(0, post.likes_count - 1)
            action = "unliked"
        else:
            # Like the post
            new_like = PostLike(post_id=post_id, user_id=current_user.id)
            db.add(new_like)
            post.likes_count += 1
            action = "liked"
        
        db.commit()
        return {"message": f"Post {action} successfully", "likes_count": post.likes_count}
        
    except Exception as e:
        logger.error("Failed to toggle like", error=str(e))
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update like"
        )

@router.post("/posts/{post_id}/comments", response_model=CommentResponse)
async def create_comment(
    post_id: str,
    comment_data: CommentCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Create a comment on a post"""
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    
    try:
        db_comment = PostComment(
            post_id=post_id,
            author_id=current_user.id,
            content=comment_data.content
        )
        
        db.add(db_comment)
        post.comments_count += 1
        db.commit()
        db.refresh(db_comment)
        
        return db_comment
        
    except Exception as e:
        logger.error("Failed to create comment", error=str(e))
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create comment"
        )

@router.get("/posts/{post_id}/comments", response_model=List[CommentResponse])
async def get_post_comments(
    post_id: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Get comments for a post"""
    comments = db.query(PostComment).filter(
        PostComment.post_id == post_id
    ).order_by(desc(PostComment.created_at)).offset(skip).limit(limit).all()
    
    return comments

@router.post("/users/{user_id}/follow")
async def toggle_follow_user(
    user_id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Follow or unfollow a user"""
    if user_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot follow yourself"
        )
    
    target_user = db.query(User).filter(User.id == user_id).first()
    if not target_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    try:
        existing_follow = db.query(UserFollow).filter(
            UserFollow.follower_id == current_user.id,
            UserFollow.following_id == user_id
        ).first()
        
        if existing_follow:
            # Unfollow
            db.delete(existing_follow)
            action = "unfollowed"
        else:
            # Follow
            new_follow = UserFollow(follower_id=current_user.id, following_id=user_id)
            db.add(new_follow)
            action = "followed"
        
        db.commit()
        return {"message": f"User {action} successfully"}
        
    except Exception as e:
        logger.error("Failed to toggle follow", error=str(e))
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update follow status"
        )
