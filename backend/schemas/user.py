"""
Pydantic schemas for user-related operations
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime

class UserBase(BaseModel):
    """Base user schema"""
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    full_name: Optional[str] = None
    bio: Optional[str] = None
    location: Optional[str] = None

class UserCreate(UserBase):
    """User creation schema"""
    password: str = Field(..., min_length=8)

class UserUpdate(BaseModel):
    """User update schema"""
    full_name: Optional[str] = None
    bio: Optional[str] = None
    location: Optional[str] = None
    profile_image_url: Optional[str] = None

class UserResponse(UserBase):
    """User response schema"""
    id: str
    profile_image_url: Optional[str] = None
    is_active: bool
    is_verified: bool
    created_at: datetime
    followers_count: Optional[int] = 0
    following_count: Optional[int] = 0
    posts_count: Optional[int] = 0
    
    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    """User login schema"""
    email: EmailStr
    password: str

class Token(BaseModel):
    """Token response schema"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int

class TokenData(BaseModel):
    """Token data schema"""
    user_id: Optional[str] = None
