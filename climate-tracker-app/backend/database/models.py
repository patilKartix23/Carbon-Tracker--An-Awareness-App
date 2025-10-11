"""
SQLAlchemy models for PostgreSQL database
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database.connection import Base
import uuid

class User(Base):
    """User model for authentication and profiles"""
    __tablename__ = "users"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    bio = Column(Text)
    location = Column(String)
    profile_image_url = Column(String)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    carbon_logs = relationship("CarbonLog", back_populates="user")
    carbon_activities = relationship("CarbonActivity", back_populates="user")
    posts = relationship("Post", back_populates="author")
    likes = relationship("PostLike", back_populates="user")
    follows_given = relationship("UserFollow", foreign_keys="UserFollow.follower_id", back_populates="follower")
    follows_received = relationship("UserFollow", foreign_keys="UserFollow.following_id", back_populates="following")

class CarbonLog(Base):
    """Carbon footprint tracking logs"""
    __tablename__ = "carbon_logs"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    date = Column(DateTime(timezone=True), nullable=False)
    
    # Carbon data (JSON format for flexibility)
    transportation_data = Column(JSON)
    energy_data = Column(JSON)
    consumption_data = Column(JSON)
    
    # Calculated values
    daily_footprint_kg_co2 = Column(Float, nullable=False)
    annual_estimate_tons_co2 = Column(Float)
    
    # Metadata
    location = Column(String)
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="carbon_logs")

class CarbonActivity(Base):
    """Individual carbon activity logs"""
    __tablename__ = "carbon_activities"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    date = Column(DateTime(timezone=True), nullable=False)
    
    # Activity details
    activity_type = Column(String, nullable=False)  # car, bus, beef, electricity, etc.
    category = Column(String, nullable=False)       # transport, food, energy, shopping
    value = Column(Float, nullable=False)           # amount (km, meals, kWh, items)
    unit = Column(String, nullable=False)           # km, meals, kWh, items
    
    # Calculated emissions
    emissions_kg_co2 = Column(Float, nullable=False)
    emission_factor = Column(Float, nullable=False)  # factor used for calculation
    
    # Optional details
    description = Column(Text)
    location = Column(String)
    
    # Social features
    is_shared = Column(Boolean, default=False)      # shared to social feed
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="carbon_activities")

class Post(Base):
    """Social media posts with climate content"""
    __tablename__ = "posts"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    author_id = Column(String, ForeignKey("users.id"), nullable=False)
    
    # Content
    caption = Column(Text)
    image_url = Column(String)
    image_analysis = Column(JSON)  # AI analysis results
    
    # Location & Climate Data
    latitude = Column(Float)
    longitude = Column(Float)
    location_name = Column(String)
    weather_data = Column(JSON)
    air_quality_data = Column(JSON)
    
    # Engagement
    likes_count = Column(Integer, default=0)
    comments_count = Column(Integer, default=0)
    
    # Metadata
    is_public = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    author = relationship("User", back_populates="posts")
    likes = relationship("PostLike", back_populates="post")
    comments = relationship("PostComment", back_populates="post")

class PostLike(Base):
    """Post likes tracking"""
    __tablename__ = "post_likes"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    post_id = Column(String, ForeignKey("posts.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="likes")
    post = relationship("Post", back_populates="likes")

class PostComment(Base):
    """Post comments"""
    __tablename__ = "post_comments"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    post_id = Column(String, ForeignKey("posts.id"), nullable=False)
    author_id = Column(String, ForeignKey("users.id"), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    post = relationship("Post", back_populates="comments")
    author = relationship("User")

class UserFollow(Base):
    """User following relationships"""
    __tablename__ = "user_follows"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    follower_id = Column(String, ForeignKey("users.id"), nullable=False)
    following_id = Column(String, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    follower = relationship("User", foreign_keys=[follower_id], back_populates="follows_given")
    following = relationship("User", foreign_keys=[following_id], back_populates="follows_received")

class SystemLog(Base):
    """System activity and error logs"""
    __tablename__ = "system_logs"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    level = Column(String, nullable=False)  # INFO, WARNING, ERROR
    service = Column(String, nullable=False)  # climate, carbon, ml, etc.
    message = Column(Text, nullable=False)
    metadata = Column(JSON)
    user_id = Column(String, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User")
