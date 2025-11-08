"""
Database models for advocacy features (petitions and impact stories)
"""
from datetime import datetime
from typing import Optional, List
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Float, Text, ForeignKey, Table, JSON
from sqlalchemy.orm import relationship
from database.connection import Base


# Association table for petition signatures
petition_signatures = Table(
    'petition_signatures',
    Base.metadata,
    Column('id', Integer, primary_key=True),
    Column('petition_id', Integer, ForeignKey('petitions.id', ondelete='CASCADE')),
    Column('user_id', Integer, ForeignKey('users.id', ondelete='CASCADE')),
    Column('signed_at', DateTime, default=datetime.utcnow),
    Column('comment', Text, nullable=True),
    Column('share_name_publicly', Boolean, default=False)
)


class Petition(Base):
    __tablename__ = 'petitions'
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(500), nullable=False)
    description = Column(Text, nullable=False)
    target = Column(String(200), nullable=False)  # Who the petition is directed to
    category = Column(String(100), nullable=False)  # e.g., "Climate Policy", "Renewable Energy"
    
    # Location data
    country = Column(String(100), nullable=True)
    state = Column(String(100), nullable=True)
    city = Column(String(100), nullable=True)
    is_global = Column(Boolean, default=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    
    # Organization info
    organization_name = Column(String(200), nullable=False)
    organization_verified = Column(Boolean, default=False)
    organization_logo_url = Column(String(500), nullable=True)
    
    # Petition details
    goal_signatures = Column(Integer, nullable=False)
    current_signatures = Column(Integer, default=0)
    deadline = Column(DateTime, nullable=True)
    status = Column(String(50), default='active')  # active, completed, closed
    
    # Impact tracking
    victory = Column(Boolean, default=False)
    victory_description = Column(Text, nullable=True)
    decision_maker_response = Column(Text, nullable=True)
    
    # Metadata
    image_url = Column(String(500), nullable=True)
    external_url = Column(String(500), nullable=True)
    tags = Column(JSON, nullable=True)  # List of tags
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Creator
    created_by_user_id = Column(Integer, ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    
    # Relationships
    updates = relationship('PetitionUpdate', back_populates='petition', cascade='all, delete-orphan')


class PetitionUpdate(Base):
    __tablename__ = 'petition_updates'
    
    id = Column(Integer, primary_key=True, index=True)
    petition_id = Column(Integer, ForeignKey('petitions.id', ondelete='CASCADE'))
    title = Column(String(300), nullable=False)
    content = Column(Text, nullable=False)
    milestone = Column(Boolean, default=False)  # Is this a milestone update?
    signatures_at_time = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    petition = relationship('Petition', back_populates='updates')


class ImpactStory(Base):
    __tablename__ = 'impact_stories'
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(300), nullable=False)
    subtitle = Column(String(500), nullable=True)
    story_type = Column(String(100), nullable=False)  # case_study, interview, day_in_life, youth_activism
    
    # Story content
    content = Column(Text, nullable=False)  # Full story in markdown or HTML
    summary = Column(Text, nullable=False)  # Short summary
    
    # Media
    featured_image_url = Column(String(500), nullable=True)
    video_url = Column(String(500), nullable=True)
    gallery_urls = Column(JSON, nullable=True)  # Array of image URLs
    
    # People & Organizations
    featured_person_name = Column(String(200), nullable=True)
    featured_person_title = Column(String(200), nullable=True)
    featured_person_photo_url = Column(String(500), nullable=True)
    organization_name = Column(String(200), nullable=True)
    
    # Location & Context
    country = Column(String(100), nullable=True)
    location_description = Column(String(300), nullable=True)
    
    # Impact metrics
    impact_metrics = Column(JSON, nullable=True)  # e.g., {"trees_planted": 1000, "co2_reduced": "500 tons"}
    
    # Categorization
    category = Column(String(100), nullable=False)  # Policy Change, Grassroots Movement, etc.
    tags = Column(JSON, nullable=True)
    related_petition_id = Column(Integer, ForeignKey('petitions.id', ondelete='SET NULL'), nullable=True)
    
    # Engagement
    views = Column(Integer, default=0)
    likes = Column(Integer, default=0)
    shares = Column(Integer, default=0)
    
    # Publishing
    published = Column(Boolean, default=True)
    featured = Column(Boolean, default=False)  # Show on homepage
    publish_date = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Author
    author_user_id = Column(Integer, ForeignKey('users.id', ondelete='SET NULL'), nullable=True)


class AdvocacyAction(Base):
    """Track user advocacy actions for gamification"""
    __tablename__ = 'advocacy_actions'
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    action_type = Column(String(100), nullable=False)  # petition_signed, story_shared, representative_contacted
    action_target_id = Column(Integer, nullable=True)  # ID of petition, story, etc.
    points_earned = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)
