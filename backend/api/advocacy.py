"""
API endpoints for advocacy features (petitions and impact stories)
"""
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_, func, desc
from typing import List, Optional
from datetime import datetime, timedelta
import math
import json
from pathlib import Path

from database.connection import get_db
from models.advocacy import Petition, PetitionUpdate, ImpactStory, AdvocacyAction, petition_signatures
from schemas.advocacy import (
    PetitionCreate, PetitionResponse, PetitionSignRequest, PetitionUpdateCreate,
    PetitionUpdateResponse, ImpactStoryCreate, ImpactStoryResponse, PetitionFilters,
    ImpactStoryFilters, AdvocacyStats, UserAdvocacyProfile, PetitionUpdate as PetitionUpdateSchema
)

router = APIRouter(prefix="/api/v1/advocacy", tags=["advocacy"])

# Load advocacy data from JSON (fallback when DB not available)
def load_advocacy_json():
    """Load petitions and stories from JSON file"""
    try:
        json_path = Path(__file__).parent.parent / 'data' / 'advocacy_data.json'
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            print(f"[Advocacy] Loaded {len(data.get('petitions', []))} petitions and {len(data.get('stories', []))} stories from JSON")
            return data
    except Exception as e:
        print(f"[Advocacy] Error loading JSON: {e}")
        return {"petitions": [], "stories": []}

# Global data store
ADVOCACY_DATA = load_advocacy_json()


# Helper function to calculate trending score
def calculate_trending_score(petition: Petition) -> float:
    """Calculate trending score based on recent activity"""
    # Get signatures in last 24 hours (simulated for now)
    days_old = (datetime.utcnow() - petition.created_at).days + 1
    signatures_per_day = petition.current_signatures / days_old
    
    # Boost score if close to goal
    progress = petition.current_signatures / petition.goal_signatures
    progress_boost = 1 + (progress * 0.5)
    
    # Boost if deadline is near
    deadline_boost = 1.0
    if petition.deadline:
        days_until_deadline = (petition.deadline - datetime.utcnow()).days
        if 0 < days_until_deadline <= 7:
            deadline_boost = 2.0
        elif 7 < days_until_deadline <= 30:
            deadline_boost = 1.5
    
    return signatures_per_day * progress_boost * deadline_boost


# Petition Endpoints
@router.get("/petitions", response_model=List[PetitionResponse])
async def get_petitions(
    category: Optional[str] = None,
    country: Optional[str] = None,
    status: str = 'active',
    is_global: Optional[bool] = None,
    victory: Optional[bool] = None,
    search: Optional[str] = None,
    sort_by: str = 'trending',
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    latitude: Optional[float] = None,
    longitude: Optional[float] = None,
    radius_km: Optional[float] = 100,
    db: Session = Depends(get_db)
):
    """Get petitions with filtering and sorting"""
    query = db.query(Petition)
    
    # Apply filters
    if status:
        query = query.filter(Petition.status == status)
    if category:
        query = query.filter(Petition.category == category)
    if country:
        query = query.filter(Petition.country == country)
    if is_global is not None:
        query = query.filter(Petition.is_global == is_global)
    if victory is not None:
        query = query.filter(Petition.victory == victory)
    
    # Search
    if search:
        search_filter = or_(
            Petition.title.ilike(f"%{search}%"),
            Petition.description.ilike(f"%{search}%"),
            Petition.organization_name.ilike(f"%{search}%")
        )
        query = query.filter(search_filter)
    
    # Location-based filtering (simplified - in production use PostGIS)
    if latitude and longitude:
        # Get petitions within radius (simplified calculation)
        all_petitions = query.all()
        nearby_petitions = []
        for petition in all_petitions:
            if petition.latitude and petition.longitude:
                # Simple distance calculation (Haversine would be better)
                lat_diff = abs(petition.latitude - latitude)
                lon_diff = abs(petition.longitude - longitude)
                distance = math.sqrt(lat_diff**2 + lon_diff**2) * 111  # Rough km conversion
                if distance <= radius_km:
                    nearby_petitions.append(petition)
        petitions = nearby_petitions
    else:
        # Sorting
        if sort_by == 'recent':
            query = query.order_by(desc(Petition.created_at))
        elif sort_by == 'signatures':
            query = query.order_by(desc(Petition.current_signatures))
        elif sort_by == 'deadline':
            query = query.filter(Petition.deadline.isnot(None)).order_by(Petition.deadline)
        else:  # trending
            query = query.order_by(desc(Petition.current_signatures))
        
        # Pagination
        offset = (page - 1) * page_size
        petitions = query.offset(offset).limit(page_size).all()
    
    # Calculate trending scores
    result = []
    for petition in petitions:
        petition_dict = PetitionResponse.from_orm(petition).dict()
        petition_dict['trending_score'] = calculate_trending_score(petition)
        result.append(PetitionResponse(**petition_dict))
    
    return result


@router.get("/petitions/{petition_id}", response_model=PetitionResponse)
async def get_petition(petition_id: int, db: Session = Depends(get_db)):
    """Get a single petition by ID"""
    petition = db.query(Petition).filter(Petition.id == petition_id).first()
    if not petition:
        raise HTTPException(status_code=404, detail="Petition not found")
    
    response = PetitionResponse.from_orm(petition)
    response.trending_score = calculate_trending_score(petition)
    return response


@router.post("/petitions", response_model=PetitionResponse, status_code=status.HTTP_201_CREATED)
async def create_petition(
    petition: PetitionCreate,
    db: Session = Depends(get_db)
):
    """Create a new petition"""
    db_petition = Petition(**petition.dict())
    db_petition.current_signatures = 0
    db_petition.status = 'active'
    
    db.add(db_petition)
    db.commit()
    db.refresh(db_petition)
    
    return PetitionResponse.from_orm(db_petition)


@router.post("/petitions/{petition_id}/sign", response_model=PetitionResponse)
async def sign_petition(
    petition_id: int,
    sign_request: PetitionSignRequest,
    user_id: int = 1,  # TODO: Get from JWT token
    db: Session = Depends(get_db)
):
    """Sign a petition"""
    petition = db.query(Petition).filter(Petition.id == petition_id).first()
    if not petition:
        raise HTTPException(status_code=404, detail="Petition not found")
    
    if petition.status != 'active':
        raise HTTPException(status_code=400, detail="Petition is not active")
    
    # Check if already signed
    existing = db.execute(
        petition_signatures.select().where(
            and_(
                petition_signatures.c.petition_id == petition_id,
                petition_signatures.c.user_id == user_id
            )
        )
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="You have already signed this petition")
    
    # Add signature
    db.execute(
        petition_signatures.insert().values(
            petition_id=petition_id,
            user_id=user_id,
            comment=sign_request.comment,
            share_name_publicly=sign_request.share_name_publicly,
            signed_at=datetime.utcnow()
        )
    )
    
    # Update signature count
    petition.current_signatures += 1
    
    # Record advocacy action
    action = AdvocacyAction(
        user_id=user_id,
        action_type='petition_signed',
        action_target_id=petition_id,
        points_earned=10
    )
    db.add(action)
    
    db.commit()
    db.refresh(petition)
    
    return PetitionResponse.from_orm(petition)


@router.get("/petitions/{petition_id}/updates", response_model=List[PetitionUpdateResponse])
async def get_petition_updates(petition_id: int, db: Session = Depends(get_db)):
    """Get updates for a petition"""
    updates = db.query(PetitionUpdate).filter(
        PetitionUpdate.petition_id == petition_id
    ).order_by(desc(PetitionUpdate.created_at)).all()
    
    return updates


@router.post("/petitions/{petition_id}/updates", response_model=PetitionUpdateResponse)
async def create_petition_update(
    petition_id: int,
    update: PetitionUpdateCreate,
    db: Session = Depends(get_db)
):
    """Create an update for a petition"""
    petition = db.query(Petition).filter(Petition.id == petition_id).first()
    if not petition:
        raise HTTPException(status_code=404, detail="Petition not found")
    
    db_update = PetitionUpdate(
        petition_id=petition_id,
        title=update.title,
        content=update.content,
        milestone=update.milestone,
        signatures_at_time=petition.current_signatures
    )
    
    db.add(db_update)
    db.commit()
    db.refresh(db_update)
    
    return db_update


# Impact Story Endpoints
@router.get("/stories", response_model=List[ImpactStoryResponse])
async def get_impact_stories(
    story_type: Optional[str] = None,
    category: Optional[str] = None,
    country: Optional[str] = None,
    featured: Optional[bool] = None,
    search: Optional[str] = None,
    sort_by: str = 'recent',
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Get impact stories with filtering and sorting"""
    query = db.query(ImpactStory).filter(ImpactStory.published == True)
    
    # Apply filters
    if story_type:
        query = query.filter(ImpactStory.story_type == story_type)
    if category:
        query = query.filter(ImpactStory.category == category)
    if country:
        query = query.filter(ImpactStory.country == country)
    if featured is not None:
        query = query.filter(ImpactStory.featured == featured)
    
    # Search
    if search:
        search_filter = or_(
            ImpactStory.title.ilike(f"%{search}%"),
            ImpactStory.summary.ilike(f"%{search}%"),
            ImpactStory.featured_person_name.ilike(f"%{search}%")
        )
        query = query.filter(search_filter)
    
    # Sorting
    if sort_by == 'popular':
        query = query.order_by(desc(ImpactStory.views), desc(ImpactStory.likes))
    elif sort_by == 'featured':
        query = query.order_by(desc(ImpactStory.featured), desc(ImpactStory.publish_date))
    else:  # recent
        query = query.order_by(desc(ImpactStory.publish_date))
    
    # Pagination
    offset = (page - 1) * page_size
    stories = query.offset(offset).limit(page_size).all()
    
    return stories


@router.get("/stories/{story_id}", response_model=ImpactStoryResponse)
async def get_impact_story(story_id: int, db: Session = Depends(get_db)):
    """Get a single impact story"""
    story = db.query(ImpactStory).filter(
        ImpactStory.id == story_id,
        ImpactStory.published == True
    ).first()
    
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")
    
    # Increment view count
    story.views += 1
    db.commit()
    db.refresh(story)
    
    return story


@router.post("/stories", response_model=ImpactStoryResponse, status_code=status.HTTP_201_CREATED)
async def create_impact_story(
    story: ImpactStoryCreate,
    db: Session = Depends(get_db)
):
    """Create a new impact story"""
    db_story = ImpactStory(**story.dict())
    
    db.add(db_story)
    db.commit()
    db.refresh(db_story)
    
    return db_story


@router.post("/stories/{story_id}/like", response_model=ImpactStoryResponse)
async def like_story(
    story_id: int,
    user_id: int = 1,  # TODO: Get from JWT token
    db: Session = Depends(get_db)
):
    """Like an impact story"""
    story = db.query(ImpactStory).filter(ImpactStory.id == story_id).first()
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")
    
    story.likes += 1
    
    # Record advocacy action
    action = AdvocacyAction(
        user_id=user_id,
        action_type='story_liked',
        action_target_id=story_id,
        points_earned=2
    )
    db.add(action)
    
    db.commit()
    db.refresh(story)
    
    return story


# Stats and Analytics
@router.get("/stats", response_model=AdvocacyStats)
async def get_advocacy_stats(
    user_id: int = 1,  # TODO: Get from JWT token
    db: Session = Depends(get_db)
):
    """Get overall advocacy statistics"""
    total_petitions = db.query(func.count(Petition.id)).scalar()
    active_petitions = db.query(func.count(Petition.id)).filter(Petition.status == 'active').scalar()
    victories = db.query(func.count(Petition.id)).filter(Petition.victory == True).scalar()
    total_signatures = db.query(func.sum(Petition.current_signatures)).scalar() or 0
    
    # User stats
    user_signatures = db.execute(
        petition_signatures.select().where(petition_signatures.c.user_id == user_id)
    ).fetchall()
    
    user_actions = db.query(AdvocacyAction).filter(AdvocacyAction.user_id == user_id).all()
    user_advocacy_points = sum(action.points_earned for action in user_actions)
    
    stories_read = db.query(func.count(AdvocacyAction.id)).filter(
        AdvocacyAction.user_id == user_id,
        AdvocacyAction.action_type == 'story_read'
    ).scalar()
    
    impact_stories_count = db.query(func.count(ImpactStory.id)).filter(
        ImpactStory.published == True
    ).scalar()
    
    return AdvocacyStats(
        total_petitions=total_petitions,
        active_petitions=active_petitions,
        victories=victories,
        total_signatures=total_signatures,
        user_signatures=len(user_signatures),
        user_advocacy_points=user_advocacy_points,
        stories_read=stories_read,
        impact_stories_count=impact_stories_count
    )


@router.get("/categories")
async def get_categories(db: Session = Depends(get_db)):
    """Get available petition categories"""
    categories = [
        "Climate Policy",
        "Renewable Energy",
        "Forest Protection",
        "Ocean Conservation",
        "Air Quality",
        "Sustainable Transportation",
        "Wildlife Protection",
        "Plastic Reduction",
        "Carbon Emissions",
        "Green Infrastructure"
    ]
    return {"categories": categories}


@router.get("/trending", response_model=List[PetitionResponse])
async def get_trending_petitions(
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    """Get trending petitions"""
    # Get active petitions from last 30 days
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    petitions = db.query(Petition).filter(
        Petition.status == 'active',
        Petition.created_at >= thirty_days_ago
    ).all()
    
    # Calculate trending scores and sort
    petition_scores = []
    for petition in petitions:
        score = calculate_trending_score(petition)
        petition_scores.append((petition, score))
    
    petition_scores.sort(key=lambda x: x[1], reverse=True)
    
    # Return top petitions
    result = []
    for petition, score in petition_scores[:limit]:
        petition_response = PetitionResponse.from_orm(petition)
        petition_response.trending_score = score
        result.append(petition_response)
    
    return result
