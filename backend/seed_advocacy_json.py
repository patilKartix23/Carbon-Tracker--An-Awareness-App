"""
Seed advocacy database with real petition and story data from JSON
"""
import json
import sys
from pathlib import Path
from datetime import datetime

# Add parent directory to path
sys.path.append(str(Path(__file__).parent))

from sqlalchemy.orm import Session
from database.connection import SessionLocal, Base, engine
from models.advocacy import Petition, ImpactStory

def load_json_data():
    """Load petition and story data from JSON file"""
    json_path = Path(__file__).parent / 'data' / 'advocacy_data.json'
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def seed_database():
    """Seed the database with petition and story data"""
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    # Load JSON data
    data = load_json_data()
    
    db = SessionLocal()
    try:
        # Clear existing data
        db.query(Petition).delete()
        db.query(ImpactStory).delete()
        db.commit()
        print("Cleared existing advocacy data")
        
        # Seed petitions
        for petition_data in data['petitions']:
            # Convert string dates to datetime
            if petition_data.get('deadline'):
                petition_data['deadline'] = datetime.fromisoformat(petition_data['deadline'].replace('Z', '+00:00'))
            if petition_data.get('created_at'):
                petition_data['created_at'] = datetime.fromisoformat(petition_data['created_at'].replace('Z', '+00:00'))
            if petition_data.get('updated_at'):
                petition_data['updated_at'] = datetime.fromisoformat(petition_data['updated_at'].replace('Z', '+00:00'))
            
            # Remove id as it will be auto-generated
            petition_id = petition_data.pop('id')
            
            petition = Petition(**petition_data)
            db.add(petition)
        
        db.commit()
        petition_count = db.query(Petition).count()
        print(f"✅ Seeded {petition_count} petitions")
        
        # Seed impact stories
        for story_data in data['stories']:
            # Convert string dates to datetime
            if story_data.get('publish_date'):
                story_data['publish_date'] = datetime.fromisoformat(story_data['publish_date'].replace('Z', '+00:00'))
            if story_data.get('created_at'):
                story_data['created_at'] = datetime.fromisoformat(story_data['created_at'].replace('Z', '+00:00'))
            
            # Remove id as it will be auto-generated
            story_id = story_data.pop('id')
            
            story = ImpactStory(**story_data)
            db.add(story)
        
        db.commit()
        story_count = db.query(ImpactStory).count()
        print(f"✅ Seeded {story_count} impact stories")
        
        print(f"\n🎉 Successfully seeded advocacy database!")
        print(f"   - {petition_count} petitions")
        print(f"   - {story_count} impact stories")
        print(f"\nYou can now access the Advocacy page with real data!")
        
    except Exception as e:
        print(f"❌ Error seeding database: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    print("🌱 Seeding advocacy database with real data...")
    seed_database()
