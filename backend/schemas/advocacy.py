"""
Pydantic schemas for advocacy features
"""
from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, validator


# Petition Schemas
class PetitionBase(BaseModel):
    title: str = Field(..., max_length=500)
    description: str
    target: str = Field(..., max_length=200)
    category: str = Field(..., max_length=100)
    country: Optional[str] = Field(None, max_length=100)
    state: Optional[str] = Field(None, max_length=100)
    city: Optional[str] = Field(None, max_length=100)
    is_global: bool = False
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    organization_name: str = Field(..., max_length=200)
    organization_verified: bool = False
    organization_logo_url: Optional[str] = None
    goal_signatures: int = Field(..., gt=0)
    deadline: Optional[datetime] = None
    image_url: Optional[str] = None
    external_url: Optional[str] = None
    tags: Optional[List[str]] = None


class PetitionCreate(PetitionBase):
    pass


class PetitionUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    victory: Optional[bool] = None
    victory_description: Optional[str] = None
    decision_maker_response: Optional[str] = None


class PetitionResponse(PetitionBase):
    id: int
    current_signatures: int
    status: str
    victory: bool
    victory_description: Optional[str]
    decision_maker_response: Optional[str]
    created_at: datetime
    updated_at: datetime
    progress_percentage: float
    trending_score: Optional[float] = 0
    user_signed: Optional[bool] = False
    
    class Config:
        from_attributes = True
    
    @validator('progress_percentage', pre=True, always=True)
    def calculate_progress(cls, v, values):
        if 'current_signatures' in values and 'goal_signatures' in values:
            if values['goal_signatures'] > 0:
                return (values['current_signatures'] / values['goal_signatures']) * 100
        return 0


class PetitionSignRequest(BaseModel):
    comment: Optional[str] = Field(None, max_length=500)
    share_name_publicly: bool = False


class PetitionUpdateCreate(BaseModel):
    title: str = Field(..., max_length=300)
    content: str
    milestone: bool = False


class PetitionUpdateResponse(BaseModel):
    id: int
    petition_id: int
    title: str
    content: str
    milestone: bool
    signatures_at_time: int
    created_at: datetime
    
    class Config:
        from_attributes = True


# Impact Story Schemas
class ImpactStoryBase(BaseModel):
    title: str = Field(..., max_length=300)
    subtitle: Optional[str] = Field(None, max_length=500)
    story_type: str = Field(..., max_length=100)
    content: str
    summary: str
    featured_image_url: Optional[str] = None
    video_url: Optional[str] = None
    gallery_urls: Optional[List[str]] = None
    featured_person_name: Optional[str] = None
    featured_person_title: Optional[str] = None
    featured_person_photo_url: Optional[str] = None
    organization_name: Optional[str] = None
    country: Optional[str] = None
    location_description: Optional[str] = None
    impact_metrics: Optional[Dict[str, Any]] = None
    category: str = Field(..., max_length=100)
    tags: Optional[List[str]] = None
    related_petition_id: Optional[int] = None
    published: bool = True
    featured: bool = False


class ImpactStoryCreate(ImpactStoryBase):
    pass


class ImpactStoryUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    summary: Optional[str] = None
    published: Optional[bool] = None
    featured: Optional[bool] = None


class ImpactStoryResponse(ImpactStoryBase):
    id: int
    views: int
    likes: int
    shares: int
    publish_date: datetime
    created_at: datetime
    updated_at: datetime
    read_time_minutes: int
    user_liked: Optional[bool] = False
    
    class Config:
        from_attributes = True
    
    @validator('read_time_minutes', pre=True, always=True)
    def calculate_read_time(cls, v, values):
        if 'content' in values:
            # Estimate 200 words per minute
            word_count = len(values['content'].split())
            return max(1, word_count // 200)
        return 5


# Filter and Search Schemas
class PetitionFilters(BaseModel):
    category: Optional[str] = None
    country: Optional[str] = None
    status: Optional[str] = 'active'
    is_global: Optional[bool] = None
    victory: Optional[bool] = None
    search: Optional[str] = None
    sort_by: str = 'trending'  # trending, recent, signatures, deadline
    page: int = Field(1, ge=1)
    page_size: int = Field(20, ge=1, le=100)


class ImpactStoryFilters(BaseModel):
    story_type: Optional[str] = None
    category: Optional[str] = None
    country: Optional[str] = None
    featured: Optional[bool] = None
    search: Optional[str] = None
    sort_by: str = 'recent'  # recent, popular, featured
    page: int = Field(1, ge=1)
    page_size: int = Field(20, ge=1, le=100)


# Advocacy Stats
class AdvocacyStats(BaseModel):
    total_petitions: int
    active_petitions: int
    victories: int
    total_signatures: int
    user_signatures: int
    user_advocacy_points: int
    stories_read: int
    impact_stories_count: int


class UserAdvocacyProfile(BaseModel):
    total_actions: int
    petitions_signed: int
    stories_shared: int
    advocacy_points: int
    badges: List[Dict[str, Any]]
    recent_actions: List[Dict[str, Any]]
