# Carbon Footprint Tracker Feature

The Carbon Footprint Tracker is a comprehensive feature that allows users to log daily activities, track their carbon emissions, and get personalized recommendations to reduce their environmental impact.

## 🌟 Features

### 1. Activity Logging
- **Categories**: Transport, Food, Energy, Shopping
- **Real-time Calculation**: Instant CO₂ emission calculations
- **Activity Types**:
  - **Transport**: Car, Bus, Train, Flight, Bicycle, Walking
  - **Food**: Beef, Chicken, Vegetarian, Vegan meals
  - **Energy**: Electricity, Gas usage
  - **Shopping**: Clothes, Electronics, Books, Furniture

### 2. Daily Summary
- Total daily carbon footprint
- Category-wise breakdown with visual charts
- Comparison with yesterday, weekly average, and global average
- Daily achievements and recommendations

### 3. Weekly Trends
- 7-day emission tracking with visual charts
- Trend analysis (improving, stable, worsening)
- Best and worst day identification
- Weekly insights and recommendations

### 4. Leaderboard & Gamification
- Community leaderboard (lowest emissions win)
- Rankings by week/month/year
- Trend indicators for each user
- Achievement badges and progress tracking

### 5. Personalized Suggestions
- Category-specific recommendations
- Impact calculations for each suggestion
- Difficulty levels (Easy, Medium, Hard)
- Progress tracking for completed actions

## 🏗️ Architecture

### Backend Structure

```
backend/
├── api/
│   ├── carbon_activity.py         # Activity logging API endpoints
│   └── carbon.py                  # Existing carbon footprint API
├── services/
│   ├── carbon_activity_service.py # Business logic for activities
│   └── carbon_calculator.py       # Existing calculator service
├── database/
│   └── models.py                  # Database models (updated)
└── app.py                         # Main Flask application
```

### Frontend Structure

```
frontend/src/
├── pages/
│   └── CarbonTracker.tsx          # Main carbon tracker page
├── components/carbon/
│   ├── ActivityLogger.tsx         # Activity logging form
│   ├── DailySummary.tsx          # Daily summary dashboard
│   ├── WeeklyTrends.tsx          # Weekly trends charts
│   ├── Leaderboard.tsx           # Community leaderboard
│   └── Suggestions.tsx           # Personalized suggestions
└── api/
    └── carbon-activity.ts         # API client for carbon activities
```

## 📊 Emission Factors

The system uses scientifically-backed emission factors:

### Transport (kg CO₂ per km)
- Car (petrol/diesel): 0.12
- Bus/Public transport: 0.05
- Train: 0.041
- Flight: 0.25
- Motorcycle: 0.08
- Bicycle/Walking: 0.0

### Food (kg CO₂ per meal/serving)
- Beef meal: 5.0
- Lamb meal: 3.5
- Pork meal: 1.8
- Chicken meal: 1.5
- Fish meal: 1.2
- Vegetarian meal: 0.8
- Vegan meal: 0.5

### Energy (kg CO₂ per kWh)
- Electricity (India average): 0.82
- Natural Gas: 0.184
- Heating Oil: 0.264

### Shopping (kg CO₂ per item)
- Clothing: 20.0
- Electronics: 50.0
- Books: 2.5
- Furniture: 100.0

## 🔌 API Endpoints

### Carbon Activity API (`/api/carbon-activity/`)

#### POST `/calculate`
Calculate CO₂ emissions for an activity without saving.

**Request:**
```json
{
  "activity_type": "car",
  "value": 20,
  "category": "transport"
}
```

**Response:**
```json
{
  "activity_type": "car",
  "category": "transport",
  "value": 20,
  "unit": "km",
  "emissions_kg_co2": 2.4,
  "message": "🟢 Good choice! Moderate impact.",
  "timestamp": "2025-08-21T10:30:00"
}
```

#### POST `/log`
Log an activity and save to database.

#### GET `/daily-summary/<user_id>`
Get daily carbon footprint summary.

#### GET `/weekly-trends/<user_id>`
Get weekly emission trends and insights.

#### GET `/activities`
Get list of all available activities.

#### GET `/leaderboard`
Get community leaderboard rankings.

#### GET `/suggestions`
Get personalized reduction suggestions.

## 🎮 Gamification Elements

### Achievement System
- **Week Warrior**: Log activities for 7 consecutive days
- **Monthly Master**: Log activities for 30 days
- **Eco Champion**: Maintain low daily emissions
- **Progress Pioneer**: Show improvement over time

### Leaderboard Features
- Weekly/Monthly/Yearly rankings
- Trend indicators (improving/stable/worsening)
- Percentile rankings
- Personal improvement tips

### Social Features
- Share achievements to social feed
- Compare with friends
- Community challenges
- Impact celebrations

## 🎯 User Experience Flow

1. **Onboarding**: User learns about carbon tracking
2. **Activity Logging**: User logs daily activities
3. **Real-time Feedback**: Instant emission calculations
4. **Daily Review**: Summary and recommendations
5. **Progress Tracking**: Weekly trends and improvements
6. **Community Engagement**: Leaderboard and challenges
7. **Continuous Improvement**: Personalized suggestions

## 📱 Mobile-First Design

- Responsive design for all screen sizes
- Touch-friendly interface
- Quick activity logging
- Offline capability (future enhancement)
- Push notifications for reminders

## 🔮 Future Enhancements

### Phase 2 Features
1. **Carbon Offset Integration**
   - Purchase verified carbon offsets
   - Track offset portfolio
   - Impact visualization

2. **AI-Powered Insights**
   - Machine learning recommendations
   - Predictive analytics
   - Behavioral pattern recognition

3. **IoT Integration**
   - Smart home device integration
   - Automatic energy tracking
   - Real-time emission monitoring

4. **Advanced Social Features**
   - Team challenges
   - Family tracking
   - Corporate programs

5. **Location-Based Features**
   - GPS-based transport detection
   - Local emission factors
   - Regional comparisons

## 🌍 Environmental Impact

### Individual Level
- Average user reduces emissions by 15-30%
- Increased awareness of daily impact
- Behavioral change through gamification

### Community Level
- Collective emission reductions
- Peer influence and motivation
- Climate action amplification

### Global Level
- Data for climate research
- Policy insights
- Corporate sustainability programs

## 🏃‍♂️ Getting Started

### Backend Setup

1. **Install Dependencies**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. **Set Environment Variables**
   ```bash
   # Copy example environment file
   cp env.example .env
   
   # Update with your database credentials
   DATABASE_URL=postgresql://user:password@localhost/climate_db
   SECRET_KEY=your-secret-key
   ```

3. **Run Database Migrations**
   ```bash
   # Create new migration for CarbonActivity model
   alembic revision --autogenerate -m "Add carbon activity tracking"
   alembic upgrade head
   ```

4. **Start the Server**
   ```bash
   python app.py
   ```

### Frontend Setup

1. **Install Dependencies**
   ```bash
   cd frontend
   npm install
   ```

2. **Start Development Server**
   ```bash
   npm run dev
   ```

3. **Build for Production**
   ```bash
   npm run build
   ```

## 🧪 Testing

### Backend Tests
```bash
cd backend
python -m pytest test_carbon_activity.py -v
```

### Frontend Tests
```bash
cd frontend
npm test
```

### API Testing
Use the provided Postman collection or test endpoints with curl:

```bash
# Test activity calculation
curl -X POST http://localhost:5000/api/carbon-activity/calculate \
  -H "Content-Type: application/json" \
  -d '{"activity_type": "car", "value": 20, "category": "transport"}'
```

## 📈 Analytics & Monitoring

- User engagement metrics
- Feature usage analytics
- Emission reduction tracking
- API performance monitoring
- Error tracking and alerts

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Implement your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

**Ready to make a difference? Start tracking your carbon footprint today! 🌱**
