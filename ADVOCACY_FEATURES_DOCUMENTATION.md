# 🌍 Advocacy & Policy Features Documentation

## Overview

The Advocacy & Policy module empowers users to take real climate action through petitions and impact stories. This comprehensive feature includes:

### ✨ Dynamic Petition Platform
- **Local & Global Petitions**: Geolocated petitions relevant to user's location
- **Trending Petitions**: Real-time algorithm highlighting urgent campaigns
- **Verified Organizations**: Trust indicators for authentic campaigns
- **Impact Tracking**: Real-time signature counters with progress visualization
- **Victory Tracking**: Success stories of past petitions
- **Automatic Notifications**: Updates when petitions reach decision-makers

### 📖 Impact Stories
- **Case Studies**: Successful advocacy campaigns and policy changes
- **Interviews**: Environmental policymakers and activists
- **Day in the Life**: Behind-the-scenes with climate advocates
- **Youth Activism**: Success stories from young climate activists
- **Impact Metrics**: Quantifiable results from advocacy efforts

## Architecture

### Backend Components

#### Models (`backend/models/advocacy.py`)
- **Petition**: Core petition data with geolocation, progress tracking, and victory status
- **PetitionUpdate**: Campaign updates and milestones
- **ImpactStory**: Inspirational stories with media galleries
- **AdvocacyAction**: User action tracking for gamification
- **petition_signatures**: Junction table for user signatures

#### API Endpoints (`backend/api/advocacy.py`)
- `GET /api/v1/advocacy/petitions` - List petitions with filters
- `GET /api/v1/advocacy/petitions/{id}` - Get petition details
- `POST /api/v1/advocacy/petitions/{id}/sign` - Sign a petition
- `GET /api/v1/advocacy/petitions/{id}/updates` - Get petition updates
- `GET /api/v1/advocacy/trending` - Get trending petitions
- `GET /api/v1/advocacy/stories` - List impact stories
- `GET /api/v1/advocacy/stories/{id}` - Get story details
- `POST /api/v1/advocacy/stories/{id}/like` - Like a story
- `GET /api/v1/advocacy/stats` - Get advocacy statistics
- `GET /api/v1/advocacy/categories` - Get available categories

#### Schemas (`backend/schemas/advocacy.py`)
- Pydantic models for validation and serialization
- Request/response models for all endpoints
- Filter models for search and pagination

### Frontend Components

#### Page (`frontend/src/pages/AdvocacyPage.tsx`)
Main advocacy hub with:
- Tabbed interface for petitions and stories
- Advanced search and filtering
- Trending sidebar
- Real-time stats dashboard
- Modal views for detailed content

#### Components
1. **PetitionCard** (`components/advocacy/PetitionCard.tsx`)
   - Displays petition summary
   - Progress bar visualization
   - Deadline countdown
   - Sign/View actions

2. **ImpactStoryCard** (`components/advocacy/ImpactStoryCard.tsx`)
   - Story preview with featured image
   - Category badges
   - Read time estimation
   - Like/Share actions

3. **PetitionModal** (`components/advocacy/PetitionModal.tsx`)
   - Full petition details
   - Campaign updates timeline
   - Sign form with optional comment
   - Victory announcements

4. **StoryModal** (`components/advocacy/StoryModal.tsx`)
   - Full story with rich media
   - Image galleries
   - Video embeds
   - Impact metrics visualization
   - Share functionality

#### Types (`frontend/src/types/advocacy.ts`)
TypeScript interfaces for:
- Petition
- ImpactStory
- PetitionUpdate
- AdvocacyStats
- Filter models

#### API Client (`frontend/src/api/advocacy.ts`)
Axios-based API client with:
- Authentication integration
- Error handling
- Type-safe requests

## Features in Detail

### 1. Dynamic Petition Platform

#### Petition Discovery
- **Trending Algorithm**: Calculates trending score based on:
  - Recent signature velocity
  - Progress toward goal
  - Proximity to deadline
  - Geographic relevance

#### Geographic Filtering
- Location-based petition discovery
- Radius search for local petitions
- Global vs. local categorization

#### Progress Tracking
- Real-time signature counters
- Visual progress bars
- Goal percentage calculation
- Milestone celebrations

#### Victory System
- Mark petitions as victories
- Victory descriptions
- Decision-maker responses
- Success story highlighting

### 2. Impact Stories

#### Story Types
1. **Case Studies**: Detailed analysis of successful campaigns
2. **Interviews**: Q&A with environmental leaders
3. **Day in the Life**: Behind-the-scenes narratives
4. **Youth Activism**: Stories highlighting young activists

#### Rich Media Support
- Featured images
- Video embeds
- Photo galleries
- Impact metric visualizations

#### Engagement Features
- View tracking
- Like system
- Share functionality
- Read time estimation

### 3. Gamification & Points

#### Advocacy Actions
- **Sign Petition**: 10 points
- **Like Story**: 2 points
- **Share Content**: 5 points
- **Create Petition**: 50 points

#### Badges & Achievements
- First Signature
- 10 Petitions Signed
- Story Ambassador (100 shares)
- Victory Contributor

## Database Schema

### Petitions Table
```sql
CREATE TABLE petitions (
    id SERIAL PRIMARY KEY,
    title VARCHAR(500) NOT NULL,
    description TEXT NOT NULL,
    target VARCHAR(200) NOT NULL,
    category VARCHAR(100) NOT NULL,
    country VARCHAR(100),
    state VARCHAR(100),
    city VARCHAR(100),
    is_global BOOLEAN DEFAULT FALSE,
    latitude FLOAT,
    longitude FLOAT,
    organization_name VARCHAR(200) NOT NULL,
    organization_verified BOOLEAN DEFAULT FALSE,
    goal_signatures INTEGER NOT NULL,
    current_signatures INTEGER DEFAULT 0,
    deadline TIMESTAMP,
    status VARCHAR(50) DEFAULT 'active',
    victory BOOLEAN DEFAULT FALSE,
    victory_description TEXT,
    image_url VARCHAR(500),
    tags JSON,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

### Impact Stories Table
```sql
CREATE TABLE impact_stories (
    id SERIAL PRIMARY KEY,
    title VARCHAR(300) NOT NULL,
    subtitle VARCHAR(500),
    story_type VARCHAR(100) NOT NULL,
    content TEXT NOT NULL,
    summary TEXT NOT NULL,
    featured_image_url VARCHAR(500),
    video_url VARCHAR(500),
    gallery_urls JSON,
    featured_person_name VARCHAR(200),
    featured_person_title VARCHAR(200),
    organization_name VARCHAR(200),
    country VARCHAR(100),
    impact_metrics JSON,
    category VARCHAR(100) NOT NULL,
    tags JSON,
    views INTEGER DEFAULT 0,
    likes INTEGER DEFAULT 0,
    featured BOOLEAN DEFAULT FALSE,
    published BOOLEAN DEFAULT TRUE,
    publish_date TIMESTAMP DEFAULT NOW(),
    created_at TIMESTAMP DEFAULT NOW()
);
```

## Setup Instructions

### 1. Backend Setup

```bash
# Navigate to backend
cd backend

# Install dependencies (if not already done)
pip install -r requirements.txt

# Run database migrations (tables will be created automatically on first run)
python main.py
```

### 2. Seed Sample Data

```bash
# Run the seed script to populate with sample petitions and stories
python seed_advocacy_data.py
```

### 3. Frontend Setup

```bash
# Navigate to frontend
cd frontend

# Install dependencies (if not already done)
npm install

# Start development server
npm run dev
```

### 4. Access the Feature

Navigate to `http://localhost:3000/advocacy` to view the Advocacy page.

## API Usage Examples

### Get Trending Petitions
```bash
curl http://localhost:8000/api/v1/advocacy/trending?limit=10
```

### Sign a Petition
```bash
curl -X POST http://localhost:8000/api/v1/advocacy/petitions/1/sign \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "comment": "I support this cause!",
    "share_name_publicly": true
  }'
```

### Get Impact Stories
```bash
curl http://localhost:8000/api/v1/advocacy/stories?category=Youth%20Activism&sort_by=popular
```

### Get Advocacy Stats
```bash
curl http://localhost:8000/api/v1/advocacy/stats \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## Filtering & Search

### Petition Filters
- **category**: Filter by category (e.g., "Climate Policy")
- **country**: Filter by country
- **status**: active, completed, closed
- **is_global**: true/false
- **victory**: true/false
- **search**: Full-text search in title and description
- **sort_by**: trending, recent, signatures, deadline
- **latitude/longitude/radius_km**: Geographic filtering

### Story Filters
- **story_type**: case_study, interview, day_in_life, youth_activism
- **category**: Filter by category
- **country**: Filter by country
- **featured**: true/false
- **search**: Full-text search
- **sort_by**: recent, popular, featured

## Customization

### Adding New Categories

Edit `backend/api/advocacy.py`:
```python
@router.get("/categories")
async def get_categories(db: Session = Depends(get_db)):
    categories = [
        "Climate Policy",
        "Renewable Energy",
        # Add your categories here
        "Your New Category",
    ]
    return {"categories": categories}
```

### Customizing Trending Algorithm

Modify `calculate_trending_score()` in `backend/api/advocacy.py`:
```python
def calculate_trending_score(petition: Petition) -> float:
    # Customize the algorithm
    days_old = (datetime.utcnow() - petition.created_at).days + 1
    signatures_per_day = petition.current_signatures / days_old
    
    # Add your custom scoring logic
    your_custom_factor = 1.0
    
    return signatures_per_day * your_custom_factor
```

### Styling

The components use Tailwind CSS. Customize colors in `tailwind.config.js`:
```js
module.exports = {
  theme: {
    extend: {
      colors: {
        'advocacy-primary': '#10b981', // Green
        'advocacy-secondary': '#3b82f6', // Blue
      }
    }
  }
}
```

## Best Practices

### For Petition Creators
1. **Clear Title**: Be specific and action-oriented
2. **Compelling Description**: Tell a story, include data
3. **Realistic Goals**: Set achievable signature targets
4. **Regular Updates**: Keep supporters informed
5. **Verified Organization**: Build trust with verification

### For Content Moderators
1. **Verify Organizations**: Confirm authenticity before verification
2. **Monitor Updates**: Ensure campaign updates are accurate
3. **Track Victories**: Celebrate and document wins
4. **Remove Duplicates**: Merge similar petitions

### For Developers
1. **Cache Trending Calculations**: Use Redis for performance
2. **Index Geographic Queries**: Add PostGIS for better location search
3. **Rate Limit Signatures**: Prevent spam with rate limiting
4. **Monitor Analytics**: Track engagement metrics

## Future Enhancements

### Phase 1 (Immediate)
- [ ] Email notifications for petition updates
- [ ] Social media share preview cards
- [ ] Petition creator dashboard
- [ ] Advanced analytics

### Phase 2 (Short-term)
- [ ] Live signature counter with WebSockets
- [ ] Campaign template library
- [ ] Integration with external petition platforms
- [ ] Mobile push notifications

### Phase 3 (Long-term)
- [ ] AI-powered petition writing assistant
- [ ] Blockchain-verified signatures
- [ ] Direct messaging with decision-makers
- [ ] Virtual town halls
- [ ] Multilingual support

## Troubleshooting

### Issue: Petitions not loading
**Solution**: Check database connection and ensure tables are created
```bash
python main.py  # This will create tables automatically
```

### Issue: Images not displaying
**Solution**: Verify image URLs are accessible and CORS is configured

### Issue: Signature count not updating
**Solution**: Check backend logs and database constraints

### Issue: TypeScript errors in frontend
**Solution**: Rebuild the project
```bash
npm run build
```

## Support & Contribution

For questions or contributions:
1. Check existing issues
2. Create detailed bug reports
3. Submit pull requests with tests
4. Follow code style guidelines

## License

This feature is part of the Climate Tracker application.

---

**Built with ❤️ for climate advocacy**

*Last Updated: October 2025*
