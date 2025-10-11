"""
Pydantic schemas for social features
"""
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime

class PostBase(BaseModel):
    """Base post schema"""
    caption: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    location_name: Optional[str] = None
    is_public: bool = True

class PostCreate(PostBase):
    """Post creation schema"""
    image_url: Optional[str] = None
    weather_data: Optional[Dict[str, Any]] = None
    air_quality_data: Optional[Dict[str, Any]] = None

class PostUpdate(BaseModel):
    """Post update schema"""
    caption: Optional[str] = None
    is_public: Optional[bool] = None

class PostResponse(PostBase):
    """Post response schema"""
    id: str
    author_id: str
    image_url: Optional[str] = None
    image_analysis: Optional[Dict[str, Any]] = None
    weather_data: Optional[Dict[str, Any]] = None
    air_quality_data: Optional[Dict[str, Any]] = None
    likes_count: int = 0
    comments_count: int = 0
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    # Author info (populated by relationship)
    author: Optional[Dict[str, Any]] = None
    
    class Config:
        from_attributes = True

class CommentBase(BaseModel):
    """Base comment schema"""
    content: str = Field(..., min_length=1, max_length=500)

class CommentCreate(CommentBase):
    """Comment creation schema"""
    pass

class CommentResponse(CommentBase):
    """Comment response schema"""
    id: str
    post_id: str
    author_id: str
    created_at: datetime
    
    # Author info
    author: Optional[Dict[str, Any]] = None
    
    class Config:
        from_attributes = True
