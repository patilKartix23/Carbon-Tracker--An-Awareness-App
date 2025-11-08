"""
Test if petition data exists in SQLite database
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.advocacy import Petition, ImpactStory

# Create SQLite engine
engine = create_engine('sqlite:///./climate_tracker.db')
SessionLocal = sessionmaker(bind=engine)

db = SessionLocal()

# Query petitions
petitions = db.query(Petition).all()
print(f"Found {len(petitions)} petitions:")
for p in petitions:
    print(f"  - {p.title} ({p.current_signatures}/{p.goal_signatures})")

# Query stories
stories = db.query(ImpactStory).all()
print(f"\nFound {len(stories)} impact stories:")
for s in stories:
    print(f"  - {s.title}")

db.close()
