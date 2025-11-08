"""
Seed script to populate advocacy data with sample petitions and impact stories
"""
from datetime import datetime, timedelta
from database.connection import SessionLocal, Base, engine
from models.advocacy import Petition, ImpactStory
import random

def seed_petitions(db):
    """Create sample petitions"""
    petitions = [
        {
            "title": "Protect Amazon Rainforest from Illegal Deforestation",
            "description": """The Amazon rainforest is being destroyed at an alarming rate. Every minute, 
an area the size of 3 football fields is cleared. We demand immediate action from the Brazilian government 
to enforce existing environmental laws, increase penalties for illegal logging, and support indigenous 
communities protecting their ancestral lands. The Amazon produces 20% of Earth's oxygen and is home to 
10% of all species on the planet. We cannot afford to lose it.""",
            "target": "Brazilian Government & Environment Ministry",
            "category": "Forest Protection",
            "country": "Brazil",
            "is_global": True,
            "organization_name": "Amazon Watch Coalition",
            "organization_verified": True,
            "goal_signatures": 500000,
            "current_signatures": 387542,
            "deadline": datetime.utcnow() + timedelta(days=45),
            "status": "active",
            "tags": ["deforestation", "rainforest", "biodiversity", "indigenous rights"]
        },
        {
            "title": "Ban Single-Use Plastics in California by 2025",
            "description": """California must lead the nation in banning single-use plastics. Every year, 
8 million tons of plastic enter our oceans, killing marine life and entering our food chain. We're calling 
on Governor Newsom to sign legislation banning plastic bags, straws, cutlery, and food containers by 2025. 
Join us in making California plastic-free!""",
            "target": "California Governor Gavin Newsom",
            "category": "Plastic Reduction",
            "country": "USA",
            "state": "California",
            "city": "Sacramento",
            "is_global": False,
            "latitude": 38.5816,
            "longitude": -121.4944,
            "organization_name": "Clean Oceans Initiative",
            "organization_verified": True,
            "goal_signatures": 250000,
            "current_signatures": 198432,
            "deadline": datetime.utcnow() + timedelta(days=30),
            "status": "active",
            "tags": ["plastic", "ocean", "california", "pollution"]
        },
        {
            "title": "Invest in Renewable Energy Infrastructure",
            "description": """We demand $500 billion investment in renewable energy infrastructure over 
the next 5 years. Solar, wind, and hydroelectric power can provide 100% of our energy needs while creating 
millions of green jobs. The technology exists - we just need political will. Tell Congress to prioritize 
renewable energy in the next infrastructure bill.""",
            "target": "U.S. Congress",
            "category": "Renewable Energy",
            "country": "USA",
            "is_global": False,
            "organization_name": "Green Energy Future",
            "organization_verified": True,
            "goal_signatures": 1000000,
            "current_signatures": 743291,
            "deadline": datetime.utcnow() + timedelta(days=60),
            "status": "active",
            "tags": ["renewable energy", "solar", "wind", "green jobs"]
        },
        {
            "title": "Save the Great Barrier Reef - Emergency Climate Action",
            "description": """The Great Barrier Reef has lost 50% of its coral in the last 3 decades due 
to climate change and ocean warming. We're calling on the Australian government to declare a climate 
emergency and commit to net-zero emissions by 2030. The reef supports 64,000 jobs and contributes $6.4 
billion to the economy. Act now before it's too late!""",
            "target": "Australian Prime Minister",
            "category": "Ocean Conservation",
            "country": "Australia",
            "is_global": True,
            "organization_name": "Reef Guardians Australia",
            "organization_verified": True,
            "goal_signatures": 300000,
            "current_signatures": 256789,
            "deadline": datetime.utcnow() + timedelta(days=25),
            "status": "active",
            "tags": ["coral reef", "ocean", "australia", "climate emergency"]
        },
        {
            "title": "End Coal Mining in National Parks",
            "description": """Coal mining operations are destroying pristine wilderness in our national 
parks. We demand an immediate halt to all coal mining permits in protected areas. These parks belong to 
the people, not mining corporations. Renewable energy makes coal obsolete - let's preserve our natural 
heritage for future generations.""",
            "target": "Department of Interior",
            "category": "Wildlife Protection",
            "country": "USA",
            "is_global": False,
            "organization_name": "National Parks Conservation Alliance",
            "organization_verified": True,
            "goal_signatures": 400000,
            "current_signatures": 401234,
            "status": "active",
            "victory": True,
            "victory_description": "Victory! The Department of Interior announced a moratorium on new coal mining permits in national parks. Your voices were heard!",
            "tags": ["coal", "mining", "national parks", "conservation"]
        }
    ]
    
    for petition_data in petitions:
        petition = Petition(**petition_data)
        db.add(petition)
    
    db.commit()
    print(f"✓ Created {len(petitions)} sample petitions")


def seed_impact_stories(db):
    """Create sample impact stories"""
    stories = [
        {
            "title": "How a 16-Year-Old Started a Global Climate Movement",
            "subtitle": "Greta Thunberg's journey from school strike to international icon",
            "story_type": "youth_activism",
            "summary": """In August 2018, 15-year-old Greta Thunberg sat alone outside Swedish parliament 
with a handmade sign reading 'School Strike for Climate.' Today, millions of young people worldwide have 
joined the Fridays for Future movement, forcing world leaders to take climate action seriously.""",
            "content": """## The Beginning

Greta Thunberg was just 15 when she decided to skip school every Friday to protest outside the Swedish 
parliament. Her demand was simple: politicians must take action on climate change.

What started as a solo protest quickly became a global phenomenon. Within months, students in over 100 
countries joined her school strikes, creating the Fridays for Future movement.

## The Impact

- Over 4 million people participated in the September 2019 global climate strike
- Greta addressed the UN Climate Action Summit
- Multiple countries declared climate emergencies in response to youth activism
- The movement changed the political discourse on climate change

## The Message

"I don't want your hope. I don't want you to be hopeful. I want you to panic. I want you to feel the fear 
I feel every day. And then I want you to act."

Greta's message resonated because it was authentic, urgent, and came from someone who would inherit the 
consequences of today's inaction.

## What We Learned

Youth activism works. When young people organize and persist, they can change the world. Greta proved that 
you don't need to be old, powerful, or famous to make a difference - you just need conviction and courage.""",
            "category": "Grassroots Movement",
            "country": "Sweden",
            "location_description": "Started in Stockholm, now global",
            "featured_person_name": "Greta Thunberg",
            "featured_person_title": "Climate Activist & Founder of Fridays for Future",
            "organization_name": "Fridays for Future",
            "impact_metrics": {
                "students_mobilized": "4+ million",
                "countries_reached": "150+",
                "climate_emergencies_declared": "30+"
            },
            "tags": ["youth activism", "school strikes", "greta thunberg", "fridays for future"],
            "views": 45678,
            "likes": 12453,
            "featured": True,
            "published": True
        },
        {
            "title": "Costa Rica: The Country Powered by 100% Renewable Energy",
            "subtitle": "How a small nation became a global leader in green energy",
            "story_type": "case_study",
            "summary": """Costa Rica has run on 100% renewable energy for over 300 days in a row. This 
small Central American nation proves that a fossil fuel-free future isn't just possible - it's profitable.""",
            "content": """## The Achievement

For more than 300 consecutive days, Costa Rica has generated 100% of its electricity from renewable 
sources. This remarkable feat makes the country a global leader in the fight against climate change.

## How They Did It

Costa Rica's success comes from a diverse mix of renewable sources:

- **Hydropower**: 78% of electricity generation
- **Geothermal**: 10%
- **Wind**: 10%
- **Solar & Biomass**: 2%

The country invested heavily in renewable infrastructure while phasing out fossil fuels. They also 
protected over 25% of their land as national parks and reserves, creating a carbon sink that absorbs 
more CO2 than the country produces.

## The Benefits

The transition to renewables has brought numerous benefits:

- Reduced air pollution and respiratory illnesses
- Created thousands of green jobs
- Made the country energy independent
- Boosted ecotourism, now 6% of GDP
- Set an example for other nations

## The Challenges

Costa Rica still faces challenges. While electricity is 100% renewable, transportation still relies on 
fossil fuels. The country is now working on electrifying public transportation and encouraging electric 
vehicle adoption.

## Lessons for the World

Costa Rica proves that renewable energy is both achievable and economically viable. With political will 
and smart planning, any country can make the transition.""",
            "category": "Policy Success",
            "country": "Costa Rica",
            "location_description": "Nationwide implementation",
            "organization_name": "Costa Rican Institute of Electricity",
            "impact_metrics": {
                "renewable_energy_percentage": "100%",
                "consecutive_days": "300+",
                "co2_reduction": "1.4 million tons/year",
                "protected_land": "25%"
            },
            "tags": ["renewable energy", "costa rica", "policy", "success story"],
            "views": 32451,
            "likes": 8765,
            "featured": True,
            "published": True
        },
        {
            "title": "A Day in the Life of a Climate Scientist",
            "subtitle": "Dr. Sarah Chen studies glacier melt in Antarctica",
            "story_type": "day_in_life",
            "summary": """Follow Dr. Sarah Chen through a typical day researching climate change in one 
of Earth's most extreme environments - Antarctica. Her work helps us understand how fast our planet is 
warming.""",
            "content": """## 5:00 AM - Wake Up

The sun never sets during Antarctic summer, so we rely on alarms. I wake up in my research station 
dormitory, where temperatures are kept at a comfortable 20°C - a stark contrast to the -30°C outside.

## 6:00 AM - Data Check

Before breakfast, I check overnight data from our automated weather stations. These sensors measure 
temperature, wind speed, and ice thickness 24/7. This morning's readings show the glacier I'm studying 
has retreated another 2 meters.

## 8:00 AM - Field Preparation

Getting ready for fieldwork in Antarctica takes time. I put on four layers, check my equipment, and 
prepare my drone for glacier surveys. Safety is paramount - one mistake out here could be fatal.

## 10:00 AM - Glacier Survey

Using drones and GPS, I map the glacier's surface. I'm documenting how quickly it's melting. This 
glacier alone contains enough ice to raise global sea levels by 5 centimeters if it completely melts.

## 2:00 PM - Ice Core Drilling

We drill deep into the ice to extract cores that contain thousands of years of climate history. Air 
bubbles trapped in these cores tell us what Earth's atmosphere was like centuries ago.

## 6:00 PM - Data Analysis

Back at the station, I analyze today's findings. The results are sobering - this glacier is melting 3 
times faster than it was 20 years ago.

## 8:00 PM - International Call

I video call with colleagues in 8 countries. Climate science is collaborative - we're all working toward 
the same goal: understanding and communicating the urgency of climate change.

## Why This Matters

Every data point we collect here helps us understand and predict climate change. My work might seem 
remote, but it affects everyone. When glaciers melt, sea levels rise, weather patterns change, and 
millions of people face displacement.""",
            "category": "Scientific Research",
            "country": "Antarctica",
            "location_description": "Antarctic Research Station",
            "featured_person_name": "Dr. Sarah Chen",
            "featured_person_title": "Glaciologist & Climate Researcher",
            "organization_name": "International Antarctic Research Institute",
            "impact_metrics": {
                "years_of_data": "10+",
                "glaciers_monitored": "15",
                "research_papers": "23"
            },
            "tags": ["climate science", "antarctica", "glaciers", "research"],
            "views": 18932,
            "likes": 4521,
            "published": True
        }
    ]
    
    for story_data in stories:
        story = ImpactStory(**story_data)
        db.add(story)
    
    db.commit()
    print(f"✓ Created {len(stories)} sample impact stories")


def main():
    """Main seed function"""
    print("🌱 Seeding advocacy data...")
    
    # Create tables if they don't exist
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        seed_petitions(db)
        seed_impact_stories(db)
        print("✅ Advocacy data seeded successfully!")
    except Exception as e:
        print(f"❌ Error seeding data: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    main()
