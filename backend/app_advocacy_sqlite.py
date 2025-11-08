"""
Advocacy API using SQLite directly (no config dependencies)
"""
from fastapi import FastAPI, Depends, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, or_, and_, func, desc
from sqlalchemy.orm import Session, sessionmaker
from typing import List, Optional
from datetime import datetime, timedelta
import math

# Import models
from models.advocacy import Petition, PetitionUpdate, ImpactStory, AdvocacyAction, petition_signatures
from schemas.advocacy import (
    PetitionResponse, ImpactStoryResponse, AdvocacyStats
)

# Create SQLite engine
SQLALCHEMY_DATABASE_URL = "sqlite:///./climate_tracker.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create FastAPI app
app = FastAPI(
    title="Climate Tracker Advocacy API",
    description="Petitions and Impact Stories for climate action",
    version="2.0.0",
    docs_url="/docs"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Helper function for trending score
def calculate_trending_score(petition: Petition) -> float:
    days_old = (datetime.utcnow() - petition.created_at).days + 1
    signatures_per_day = petition.current_signatures / days_old
    progress = petition.current_signatures / petition.goal_signatures
    progress_boost = 1 + (progress * 0.5)
    
    deadline_boost = 1.0
    if petition.deadline:
        days_until_deadline = (petition.deadline - datetime.utcnow()).days
        if 0 < days_until_deadline <= 7:
            deadline_boost = 2.0
        elif 7 < days_until_deadline <= 30:
            deadline_boost = 1.5
    
    return signatures_per_day * progress_boost * deadline_boost

# Root endpoint
@app.get("/")
async def root():
    return {
        "service": "Climate Tracker Advocacy API",
        "version": "2.0.0",
        "status": "running",
        "database": "SQLite",
        "endpoints": {
            "petitions": "/api/v1/advocacy/petitions",
            "stories": "/api/v1/advocacy/stories",
            "docs": "/docs"
        }
    }

# Health check
@app.get("/health")
async def health():
    return {"status": "healthy", "database": "SQLite"}

# Get petitions
@app.get("/api/v1/advocacy/petitions", response_model=List[PetitionResponse])
async def get_petitions(
    category: Optional[str] = None,
    status_filter: str = Query('active', alias='status'),
    search: Optional[str] = None,
    sort_by: str = 'trending',
    page: int = 1,
    page_size: int = 20,
    db: Session = Depends(get_db)
):
    query = db.query(Petition)
    
    if status_filter:
        query = query.filter(Petition.status == status_filter)
    if category:
        query = query.filter(Petition.category == category)
    if search:
        query = query.filter(or_(
            Petition.title.like(f"%{search}%"),
            Petition.description.like(f"%{search}%")
        ))
    
    if sort_by == 'recent':
        query = query.order_by(desc(Petition.created_at))
    elif sort_by == 'signatures':
        query = query.order_by(desc(Petition.current_signatures))
    else:
        query = query.order_by(desc(Petition.current_signatures))
    
    offset = (page - 1) * page_size
    petitions = query.offset(offset).limit(page_size).all()
    
    result = []
    for petition in petitions:
        p_dict = {
            **{c.name: getattr(petition, c.name) for c in petition.__table__.columns},
            'progress_percentage': (petition.current_signatures / petition.goal_signatures * 100) if petition.goal_signatures > 0 else 0,
            'trending_score': calculate_trending_score(petition),
            'user_signed': False
        }
        result.append(PetitionResponse(**p_dict))
    
    return result

# Get single petition
@app.get("/api/v1/advocacy/petitions/{petition_id}", response_model=PetitionResponse)
async def get_petition(petition_id: int, db: Session = Depends(get_db)):
    petition = db.query(Petition).filter(Petition.id == petition_id).first()
    if not petition:
        raise HTTPException(status_code=404, detail="Petition not found")
    
    p_dict = {
        **{c.name: getattr(petition, c.name) for c in petition.__table__.columns},
        'progress_percentage': (petition.current_signatures / petition.goal_signatures * 100) if petition.goal_signatures > 0 else 0,
        'trending_score': calculate_trending_score(petition),
        'user_signed': False
    }
    return PetitionResponse(**p_dict)

# Get impact stories
@app.get("/api/v1/advocacy/stories", response_model=List[ImpactStoryResponse])
async def get_stories(
    story_type: Optional[str] = None,
    category: Optional[str] = None,
    search: Optional[str] = None,
    sort_by: str = 'recent',
    page: int = 1,
    page_size: int = 20,
    db: Session = Depends(get_db)
):
    query = db.query(ImpactStory).filter(ImpactStory.published == True)
    
    if story_type:
        query = query.filter(ImpactStory.story_type == story_type)
    if category:
        query = query.filter(ImpactStory.category == category)
    if search:
        query = query.filter(or_(
            ImpactStory.title.like(f"%{search}%"),
            ImpactStory.summary.like(f"%{search}%")
        ))
    
    if sort_by == 'popular':
        query = query.order_by(desc(ImpactStory.views))
    else:
        query = query.order_by(desc(ImpactStory.publish_date))
    
    offset = (page - 1) * page_size
    stories = query.offset(offset).limit(page_size).all()
    
    result = []
    for story in stories:
        s_dict = {
            **{c.name: getattr(story, c.name) for c in story.__table__.columns},
            'read_time_minutes': max(1, len(story.content.split()) // 200),
            'user_liked': False
        }
        result.append(ImpactStoryResponse(**s_dict))
    
    return result

# Get single story
@app.get("/api/v1/advocacy/stories/{story_id}", response_model=ImpactStoryResponse)
async def get_story(story_id: int, db: Session = Depends(get_db)):
    story = db.query(ImpactStory).filter(ImpactStory.id == story_id).first()
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")
    
    # Increment views
    story.views += 1
    db.commit()
    db.refresh(story)
    
    s_dict = {
        **{c.name: getattr(story, c.name) for c in story.__table__.columns},
        'read_time_minutes': max(1, len(story.content.split()) // 200),
        'user_liked': False
    }
    return ImpactStoryResponse(**s_dict)

# Get stats
@app.get("/api/v1/advocacy/stats", response_model=AdvocacyStats)
async def get_stats(db: Session = Depends(get_db)):
    total_petitions = db.query(func.count(Petition.id)).scalar()
    active_petitions = db.query(func.count(Petition.id)).filter(Petition.status == 'active').scalar()
    victories = db.query(func.count(Petition.id)).filter(Petition.victory == True).scalar()
    total_signatures = db.query(func.sum(Petition.current_signatures)).scalar() or 0
    impact_stories_count = db.query(func.count(ImpactStory.id)).filter(ImpactStory.published == True).scalar()
    
    return AdvocacyStats(
        total_petitions=total_petitions,
        active_petitions=active_petitions,
        victories=victories,
        total_signatures=total_signatures,
        user_signatures=0,
        user_advocacy_points=0,
        stories_read=0,
        impact_stories_count=impact_stories_count
    )

# Get categories
@app.get("/api/v1/advocacy/categories")
async def get_categories():
    categories = [
        "Climate Policy", "Renewable Energy", "Forest Protection",
        "Ocean Conservation", "Air Quality", "Sustainable Transportation",
        "Wildlife Protection", "Plastic Reduction", "Carbon Emissions", "Green Infrastructure"
    ]
    return {"categories": categories}

# Get trending petitions
@app.get("/api/v1/advocacy/trending", response_model=List[PetitionResponse])
async def get_trending(limit: int = 10, db: Session = Depends(get_db)):
    petitions = db.query(Petition).filter(Petition.status == 'active').limit(50).all()
    
    petition_scores = []
    for petition in petitions:
        score = calculate_trending_score(petition)
        petition_scores.append((petition, score))
    
    petition_scores.sort(key=lambda x: x[1], reverse=True)
    
    result = []
    for petition, score in petition_scores[:limit]:
        p_dict = {
            **{c.name: getattr(petition, c.name) for c in petition.__table__.columns},
            'progress_percentage': (petition.current_signatures / petition.goal_signatures * 100) if petition.goal_signatures > 0 else 0,
            'trending_score': score,
            'user_signed': False
        }
        result.append(PetitionResponse(**p_dict))
    
    return result

if __name__ == "__main__":
    import uvicorn
    print("=" * 60)
    print("🚀 Climate Tracker Advocacy API (SQLite)")
    print("=" * 60)
    print("Server: http://localhost:8000")
    print("Docs: http://localhost:8000/docs")
    print("Database: SQLite (climate_tracker.db)")
    print("=" * 60)
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
