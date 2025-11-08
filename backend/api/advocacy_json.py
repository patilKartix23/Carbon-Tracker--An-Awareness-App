"""
Advocacy API endpoints using JSON data (fallback when database not available)
Real petitions and impact stories from advocacy_data.json
"""
from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from datetime import datetime
import json
from pathlib import Path

router = APIRouter(prefix="/api/v1/advocacy", tags=["advocacy"])

# Load advocacy data from JSON
def load_advocacy_json():
    """Load petitions and stories from JSON file"""
    try:
        json_path = Path(__file__).parent.parent / 'data' / 'advocacy_data.json'
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            print(f"[Advocacy JSON] Loaded {len(data.get('petitions', []))} petitions and {len(data.get('stories', []))} stories")
            return data
    except Exception as e:
        print(f"[Advocacy JSON] Error loading: {e}")
        return {"petitions": [], "stories": []}

ADVOCACY_DATA = load_advocacy_json()

def calculate_trending_score_json(petition: dict) -> float:
    """Calculate trending score for JSON petition data"""
    try:
        created_at = datetime.fromisoformat(petition['created_at'].replace('Z', '+00:00'))
        days_old = (datetime.utcnow() - created_at).days + 1
        signatures_per_day = petition['current_signatures'] / max(days_old, 1)
        
        progress = petition['current_signatures'] / petition['goal_signatures']
        progress_boost = 1 + (progress * 0.5)
        
        deadline_boost = 1.0
        if petition.get('deadline'):
            deadline = datetime.fromisoformat(petition['deadline'].replace('Z', '+00:00'))
            days_until_deadline = (deadline - datetime.utcnow()).days
            if 0 < days_until_deadline <= 7:
                deadline_boost = 2.0
            elif 7 < days_until_deadline <= 30:
                deadline_boost = 1.5
        
        return signatures_per_day * progress_boost * deadline_boost
    except:
        return 0.0

@router.get("/petitions")
async def get_petitions(
    category: Optional[str] = None,
    country: Optional[str] = None,
    status: str = 'active',
    is_global: Optional[bool] = None,
    victory: Optional[bool] = None,
    search: Optional[str] = None,
    sort_by: str = 'trending',
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100)
):
    """Get petitions with filtering"""
    petitions = ADVOCACY_DATA.get('petitions', []).copy()
    
    # Apply filters
    if status:
        petitions = [p for p in petitions if p.get('status') == status]
    if category:
        petitions = [p for p in petitions if p.get('category') == category]
    if country:
        petitions = [p for p in petitions if p.get('country') == country]
    if is_global is not None:
        petitions = [p for p in petitions if p.get('is_global') == is_global]
    if victory is not None:
        petitions = [p for p in petitions if p.get('victory') == victory]
    if search:
        search_lower = search.lower()
        petitions = [p for p in petitions if 
                    search_lower in p.get('title', '').lower() or
                    search_lower in p.get('description', '').lower()]
    
    # Calculate trending scores and add to petitions
    for petition in petitions:
        petition['trending_score'] = calculate_trending_score_json(petition)
    
    # Sort
    if sort_by == 'recent':
        petitions.sort(key=lambda x: x.get('created_at', ''), reverse=True)
    elif sort_by == 'signatures':
        petitions.sort(key=lambda x: x.get('current_signatures', 0), reverse=True)
    elif sort_by == 'trending':
        petitions.sort(key=lambda x: x.get('trending_score', 0), reverse=True)
    
    # Pagination
    start_idx = (page - 1) * page_size
    end_idx = start_idx + page_size
    
    return petitions[start_idx:end_idx]

@router.get("/petitions/{petition_id}")
async def get_petition(petition_id: int):
    """Get single petition"""
    petition = next((p for p in ADVOCACY_DATA.get('petitions', []) if p['id'] == petition_id), None)
    if not petition:
        raise HTTPException(status_code=404, detail="Petition not found")
    
    petition_copy = petition.copy()
    petition_copy['trending_score'] = calculate_trending_score_json(petition)
    return petition_copy

@router.get("/trending")
async def get_trending_petitions(limit: int = Query(10, ge=1, le=50)):
    """Get trending petitions"""
    petitions = [p for p in ADVOCACY_DATA.get('petitions', []) if p.get('status') == 'active']
    
    for petition in petitions:
        petition['trending_score'] = calculate_trending_score_json(petition)
    
    petitions.sort(key=lambda x: x.get('trending_score', 0), reverse=True)
    return petitions[:limit]

@router.get("/stories")
async def get_stories(
    story_type: Optional[str] = None,
    category: Optional[str] = None,
    country: Optional[str] = None,
    featured: Optional[bool] = None,
    search: Optional[str] = None,
    sort_by: str = 'recent',
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100)
):
    """Get impact stories with filtering"""
    stories = ADVOCACY_DATA.get('stories', []).copy()
    
    # Apply filters
    if story_type:
        stories = [s for s in stories if s.get('story_type') == story_type]
    if category:
        stories = [s for s in stories if s.get('category') == category]
    if country:
        stories = [s for s in stories if s.get('country') == country]
    if featured is not None:
        stories = [s for s in stories if s.get('featured') == featured]
    if search:
        search_lower = search.lower()
        stories = [s for s in stories if 
                  search_lower in s.get('title', '').lower() or
                  search_lower in s.get('content', '').lower()]
    
    # Sort
    if sort_by == 'recent':
        stories.sort(key=lambda x: x.get('publish_date', ''), reverse=True)
    elif sort_by == 'popular':
        stories.sort(key=lambda x: x.get('likes', 0) + x.get('views', 0), reverse=True)
    elif sort_by == 'featured':
        stories.sort(key=lambda x: (x.get('featured', False), x.get('publish_date', '')), reverse=True)
    
    # Pagination
    start_idx = (page - 1) * page_size
    end_idx = start_idx + page_size
    
    return stories[start_idx:end_idx]

@router.get("/stories/{story_id}")
async def get_story(story_id: int):
    """Get single story"""
    story = next((s for s in ADVOCACY_DATA.get('stories', []) if s['id'] == story_id), None)
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")
    return story

@router.post("/petitions/{petition_id}/sign")
async def sign_petition(petition_id: int, signature_data: dict):
    """Sign a petition (simulated)"""
    petition = next((p for p in ADVOCACY_DATA.get('petitions', []) if p['id'] == petition_id), None)
    if not petition:
        raise HTTPException(status_code=404, detail="Petition not found")
    
    # Simulate signing (in real app, would update database)
    petition['current_signatures'] += 1
    
    return {
        "success": True,
        "message": "Petition signed successfully!",
        "current_signatures": petition['current_signatures']
    }

@router.post("/stories/{story_id}/like")
async def like_story(story_id: int):
    """Like a story (simulated)"""
    story = next((s for s in ADVOCACY_DATA.get('stories', []) if s['id'] == story_id), None)
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")
    
    # Simulate liking (in real app, would update database)
    story['likes'] = story.get('likes', 0) + 1
    
    return {
        "success": True,
        "message": "Story liked!",
        "likes": story['likes']
    }

@router.get("/stats")
async def get_stats():
    """Get advocacy statistics"""
    petitions = ADVOCACY_DATA.get('petitions', [])
    stories = ADVOCACY_DATA.get('stories', [])
    
    active_petitions = [p for p in petitions if p.get('status') == 'active']
    victories = [p for p in petitions if p.get('victory')]
    
    total_signatures = sum(p.get('current_signatures', 0) for p in petitions)
    total_views = sum(s.get('views', 0) for s in stories)
    
    return {
        "total_petitions": len(petitions),
        "active_petitions": len(active_petitions),
        "victories": len(victories),
        "total_signatures": total_signatures,
        "total_stories": len(stories),
        "total_story_views": total_views,
        "user_signatures": 0,  # Would come from user auth
        "user_stories_liked": 0  # Would come from user auth
    }

@router.get("/categories")
async def get_categories():
    """Get available categories"""
    return {
        "categories": [
            "Climate Policy",
            "Renewable Energy",
            "Forest Conservation",
            "Wildlife Protection",
            "Water Conservation",
            "Air Quality",
            "Waste Management",
            "Sustainable Transport",
            "Ocean Conservation",
            "Youth Activism"
        ]
    }
