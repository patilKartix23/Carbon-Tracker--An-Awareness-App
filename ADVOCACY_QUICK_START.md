# 🚀 Advocacy Features - Quick Start Guide

## What Was Implemented

Your Climate Tracker app now includes a comprehensive **Advocacy & Policy** module with:

### ✅ Dynamic Petition Platform
- **Petition Discovery**: Browse and filter petitions by category, location, and trending status
- **Sign Petitions**: Users can sign petitions with optional comments
- **Progress Tracking**: Real-time signature counters with visual progress bars
- **Victory System**: Track successful campaigns and their outcomes
- **Geolocation**: Find petitions relevant to your location
- **Trending Algorithm**: Smart algorithm highlights urgent campaigns

### ✅ Impact Stories
- **Story Types**: Case studies, interviews, day-in-the-life, youth activism
- **Rich Media**: Featured images, video embeds, photo galleries
- **Impact Metrics**: Visual display of quantifiable results
- **Engagement**: Like, share, and track story views
- **Featured Content**: Highlight important stories

### ✅ Full-Stack Implementation
- **Backend**: FastAPI with PostgreSQL database
- **Frontend**: React + TypeScript with Tailwind CSS
- **Navigation**: Integrated into main app navigation
- **Responsive**: Works on desktop and mobile

## Files Created

### Backend (10 files)
```
backend/
├── models/advocacy.py              # Database models
├── schemas/advocacy.py             # Pydantic schemas
├── api/advocacy.py                 # API endpoints (17 endpoints)
└── seed_advocacy_data.py           # Sample data script
```

### Frontend (7 files)
```
frontend/src/
├── pages/AdvocacyPage.tsx          # Main advocacy page
├── components/advocacy/
│   ├── PetitionCard.tsx            # Petition card component
│   ├── ImpactStoryCard.tsx         # Story card component
│   ├── PetitionModal.tsx           # Petition detail modal
│   └── StoryModal.tsx              # Story detail modal
├── types/advocacy.ts               # TypeScript types
└── api/advocacy.ts                 # API client functions
```

### Configuration Updates
- `backend/main.py` - Added advocacy router
- `frontend/src/App.tsx` - Added advocacy route
- `frontend/src/components/layout/Navbar.tsx` - Added navigation link

## How to Run

### Step 1: Start Backend
```bash
cd backend
python main.py
```
The backend will automatically create database tables on first run.

### Step 2: Seed Sample Data (Optional but Recommended)
```bash
cd backend
python seed_advocacy_data.py
```
This creates:
- 5 sample petitions (including 1 victory)
- 3 impact stories (youth activism, case study, day-in-life)

### Step 3: Start Frontend
```bash
cd frontend
npm run dev
```

### Step 4: Access Advocacy Features
Open your browser and navigate to:
- Main app: `http://localhost:3000`
- Advocacy page: `http://localhost:3000/advocacy`
- API docs: `http://localhost:8000/docs`

## User Journey

### Browsing Petitions
1. Click **"Advocacy"** in the navigation bar
2. Browse trending petitions in the sidebar
3. Filter by category (e.g., "Forest Protection", "Renewable Energy")
4. Search for specific topics
5. Sort by trending, recent, or signature count

### Signing a Petition
1. Click on a petition card to view details
2. Read the full description and updates
3. Add an optional comment
4. Click **"Sign Petition"**
5. Your signature is recorded and count updates

### Reading Impact Stories
1. Switch to **"Impact Stories"** tab
2. Browse by story type (Youth Activism, Interviews, etc.)
3. Click **"Read Story"** to view full content
4. Like and share stories you find inspiring
5. View impact metrics showing real results

## Key Features Demo

### Petition Features
- ✨ **Trending Badge**: Shows hot petitions
- 🎯 **Progress Bar**: Visual signature progress
- ⏰ **Deadline Countdown**: Days remaining
- 🏆 **Victory Banner**: Successful campaigns
- 📍 **Location Tags**: Local vs. global
- ✓ **Verified Organizations**: Trust indicators
- 💬 **Comments**: Share why you signed

### Story Features
- 🌟 **Featured Stories**: Highlighted content
- 📖 **Read Time**: Estimated reading duration
- 🖼️ **Media Galleries**: Multiple images
- 🎥 **Video Embeds**: YouTube/Vimeo support
- 📊 **Impact Metrics**: Quantified results
- ❤️ **Like System**: Show support
- 📤 **Share**: Social media integration

## API Endpoints Overview

### Petitions
- `GET /api/v1/advocacy/petitions` - List all petitions
- `GET /api/v1/advocacy/petitions/{id}` - Get petition details
- `POST /api/v1/advocacy/petitions/{id}/sign` - Sign a petition
- `GET /api/v1/advocacy/trending` - Get trending petitions
- `GET /api/v1/advocacy/categories` - Get available categories

### Impact Stories
- `GET /api/v1/advocacy/stories` - List all stories
- `GET /api/v1/advocacy/stories/{id}` - Get story details
- `POST /api/v1/advocacy/stories/{id}/like` - Like a story

### Statistics
- `GET /api/v1/advocacy/stats` - Get user advocacy stats

## Testing the Features

### Test Scenario 1: Sign a Petition
```bash
# View petitions
curl http://localhost:8000/api/v1/advocacy/petitions

# Sign petition ID 1
curl -X POST http://localhost:8000/api/v1/advocacy/petitions/1/sign \
  -H "Content-Type: application/json" \
  -d '{"comment": "I support this!", "share_name_publicly": true}'
```

### Test Scenario 2: View Trending
```bash
# Get top 5 trending petitions
curl http://localhost:8000/api/v1/advocacy/trending?limit=5
```

### Test Scenario 3: Read Stories
```bash
# Get youth activism stories
curl http://localhost:8000/api/v1/advocacy/stories?story_type=youth_activism
```

## Sample Data Included

### Petitions
1. **Protect Amazon Rainforest** - Global, 387K signatures
2. **Ban Single-Use Plastics in California** - Local, 198K signatures
3. **Invest in Renewable Energy** - National, 743K signatures
4. **Save the Great Barrier Reef** - Australia, 256K signatures
5. **End Coal Mining in National Parks** - ✅ VICTORY, 401K signatures

### Impact Stories
1. **Greta Thunberg's Climate Movement** - Youth activism story
2. **Costa Rica's 100% Renewable Energy** - Policy success case study
3. **A Day in the Life of a Climate Scientist** - Behind-the-scenes

## Customization

### Change Colors
Edit `frontend/src/pages/AdvocacyPage.tsx`:
```tsx
// Change primary color from green to blue
className="bg-green-600" // Change to bg-blue-600
```

### Add New Categories
Edit `backend/api/advocacy.py`:
```python
categories = [
    "Climate Policy",
    "Your New Category",  # Add here
]
```

### Adjust Trending Algorithm
Modify `calculate_trending_score()` in `backend/api/advocacy.py`

## Production Considerations

### Before Deploying
1. **Database**: Ensure PostgreSQL is properly configured
2. **Environment Variables**: Set up .env with production values
3. **CORS**: Update allowed origins in backend
4. **Authentication**: Connect to real user authentication
5. **Rate Limiting**: Add rate limits on signature endpoints
6. **Image Storage**: Use CDN for petition/story images
7. **Email Notifications**: Set up email service for updates

### Security
- Validate all user inputs
- Sanitize HTML content in stories
- Implement CSRF protection
- Add captcha for petition signatures
- Rate limit API calls

## Next Steps

### Immediate
1. ✅ Test all features in your browser
2. ✅ Sign a sample petition
3. ✅ Read an impact story
4. ✅ Check API documentation at `/docs`

### Short-term
- Add email notifications for petition updates
- Implement social media sharing preview cards
- Create admin dashboard for petition management
- Add more sample data

### Long-term
- Build mobile app version
- Add live signature counter with WebSockets
- Integrate with external petition platforms
- Implement blockchain-verified signatures

## Troubleshooting

### Petitions not showing?
- Check backend is running: `http://localhost:8000/health`
- Verify database tables created: Check backend logs
- Run seed script: `python seed_advocacy_data.py`

### TypeScript errors?
- Restart frontend dev server: `npm run dev`
- Clear node_modules and reinstall: `npm install`

### Database errors?
- Ensure PostgreSQL is running
- Check database credentials in `.env`
- Tables auto-create on first backend run

## Support

For issues or questions:
1. Check `ADVOCACY_FEATURES_DOCUMENTATION.md` for detailed docs
2. Review API docs at `http://localhost:8000/docs`
3. Check browser console for frontend errors
4. Check backend logs for API errors

---

## 🎉 Success!

You now have a fully functional Advocacy & Policy module that allows users to:
- ✅ Discover and sign petitions
- ✅ Read inspiring impact stories
- ✅ Track campaign progress
- ✅ Engage with climate action

**Your users can now move from awareness to action!**

Built with ❤️ for climate advocacy
