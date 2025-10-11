"""
Carbon footprint API routes (FastAPI version)
"""
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Dict, Any, Optional
import structlog
from datetime import datetime
from sqlalchemy.orm import Session

from services.carbon_calculator import CarbonFootprintCalculator
from api.auth import get_current_active_user
from database.connection import get_db
from database.models import User, CarbonLog, CarbonActivity

logger = structlog.get_logger()
router = APIRouter()
carbon_calculator = CarbonFootprintCalculator()

# Comprehensive emission factors (kg CO₂ per unit)
EMISSION_FACTORS = {
    # Transportation (per km)
    "car": 0.12,  # petrol car
    "car_diesel": 0.11,
    "bus": 0.05,
    "train": 0.04,
    "metro": 0.03,
    "bike": 0.0,  # bicycle
    "motorbike": 0.08,
    "flight_domestic": 0.25,  # short-haul
    "flight_international": 0.18,  # long-haul (more efficient per km)
    "auto_rickshaw": 0.07,
    
    # Food (per meal/serving)
    "beef": 5.0,
    "lamb": 4.5,
    "pork": 2.5,
    "chicken": 1.5,
    "fish": 1.2,
    "vegetarian": 0.8,
    "vegan": 0.5,
    "dairy": 1.0,  # per glass of milk
    "cheese": 2.0,  # per serving
    
    # Energy (per kWh or unit)
    "electricity_india": 0.82,  # India's grid average
    "electricity_renewable": 0.05,
    "natural_gas": 0.18,  # per kWh
    "lpg_cooking": 2.3,  # per kg
    "water_heating": 0.5,  # per usage
    
    # Shopping/Consumption (per item or unit)
    "clothes_new": 20.0,  # per clothing item
    "clothes_secondhand": 2.0,
    "smartphone": 85.0,  # per device
    "laptop": 150.0,
    "book": 1.0,
    "plastic_bottle": 0.5,
    "paper_waste": 0.1,  # per kg
    "food_waste": 2.5,  # per kg
    
    # Household
    "waste_general": 0.5,  # per kg
    "water_usage": 0.0003,  # per liter
}

class CarbonFootprintRequest(BaseModel):
    """Carbon footprint calculation request"""
    transportation: Optional[Dict[str, float]] = {}
    energy: Optional[Dict[str, float]] = {}
    consumption: Optional[Dict[str, float]] = {}
    location: Optional[str] = None
    save_to_profile: bool = False

class SimpleCarbonRequest(BaseModel):
    """Simplified carbon footprint request"""
    car_miles: Optional[float] = 0
    electricity_kwh: Optional[float] = 0
    flights_hours: Optional[float] = 0

class ActivityRequest(BaseModel):
    """Single activity carbon footprint request"""
    activity_type: str
    value: float
    unit: Optional[str] = None  # km, meal, kWh, item, etc.
    description: Optional[str] = None

class ActivityResponse(BaseModel):
    """Activity carbon footprint response"""
    activity_type: str
    value: float
    unit: str
    emissions_kg_co2: float
    description: Optional[str]
    timestamp: str
    suggestions: list[str] = []

@router.post("/calculate")
async def calculate_carbon_footprint(
    request: CarbonFootprintRequest,
    current_user: Optional[User] = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Calculate comprehensive carbon footprint"""
    try:
        # Prepare data for calculator
        data = {
            'transportation': request.transportation,
            'energy': request.energy,
            'consumption': request.consumption,
            'location': request.location
        }
        
        # Calculate footprint using the enhanced calculator
        footprint_result = carbon_calculator.calculate_total_footprint(data)
        
        # Get personalized recommendations
        recommendations = carbon_calculator.get_personalized_recommendations(
            footprint_result, 
            request.location
        )
        
        # Compare to averages
        comparison = carbon_calculator.compare_to_averages(
            footprint_result['daily_footprint_kg_co2']
        )
        
        # Save to user profile if requested and user is authenticated
        if request.save_to_profile and current_user:
            try:
                carbon_log = CarbonLog(
                    user_id=current_user.id,
                    date=datetime.utcnow(),
                    transportation_data=request.transportation,
                    energy_data=request.energy,
                    consumption_data=request.consumption,
                    daily_footprint_kg_co2=footprint_result['daily_footprint_kg_co2'],
                    annual_estimate_tons_co2=footprint_result['annual_estimate_tons_co2'],
                    location=request.location,
                    notes=f"Calculated via API on {datetime.utcnow().isoformat()}"
                )
                
                db.add(carbon_log)
                db.commit()
                logger.info("Carbon footprint saved to profile", 
                           user_id=current_user.id, 
                           footprint=footprint_result['daily_footprint_kg_co2'])
            except Exception as e:
                logger.error("Failed to save carbon log", error=str(e))
                # Don't fail the request if saving fails
        
        logger.info("Carbon footprint calculated", 
                   footprint=footprint_result['daily_footprint_kg_co2'],
                   user_id=current_user.id if current_user else None)
        
        return {
            "status": "success",
            "footprint": footprint_result,
            "recommendations": recommendations,
            "comparison": comparison,
            "saved_to_profile": request.save_to_profile and current_user is not None,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    except Exception as e:
        logger.error("Error calculating carbon footprint", error=str(e))
        raise HTTPException(
            status_code=500,
            detail=f"Failed to calculate carbon footprint: {str(e)}"
        )

@router.post("/simple")
async def calculate_simple_footprint(
    request: SimpleCarbonRequest,
    current_user: Optional[User] = Depends(get_current_active_user)
):
    """Simplified carbon footprint calculation"""
    try:
        # Convert to standard format
        standard_data = {
            'transportation': {},
            'energy': {}
        }
        
        # Handle transportation
        if request.car_miles and request.car_miles > 0:
            standard_data['transportation']['car_gasoline'] = request.car_miles
        
        if request.flights_hours and request.flights_hours > 0:
            # Rough conversion: 1 hour flight ≈ 500 miles
            standard_data['transportation']['flight_domestic'] = request.flights_hours * 500
        
        # Handle energy
        if request.electricity_kwh and request.electricity_kwh > 0:
            standard_data['energy']['electricity_grid'] = request.electricity_kwh
        
        # Calculate using enhanced calculator
        footprint_result = carbon_calculator.calculate_total_footprint(standard_data)
        recommendations = carbon_calculator.get_personalized_recommendations(footprint_result)
        
        logger.info("Simple carbon footprint calculated", 
                   footprint=footprint_result['daily_footprint_kg_co2'],
                   user_id=current_user.id if current_user else None)
        
        # Return simplified response for backward compatibility
        return {
            "status": "success",
            "daily_footprint_lbs_co2": footprint_result['daily_footprint_lbs_co2'],
            "daily_footprint_kg_co2": footprint_result['daily_footprint_kg_co2'],
            "annual_estimate_tons_co2": footprint_result['annual_estimate_tons_co2'],
            "breakdown": {
                "transportation": footprint_result['breakdown']['transportation']['total_kg_co2'],
                "energy": footprint_result['breakdown']['energy']['total_kg_co2']
            },
            "recommendations": recommendations[:3],  # Top 3 for simple version
            "timestamp": datetime.utcnow().isoformat()
        }
    
    except Exception as e:
        logger.error("Error calculating simple footprint", error=str(e))
        raise HTTPException(
            status_code=500,
            detail=f"Failed to calculate footprint: {str(e)}"
        )

@router.get("/history")
async def get_carbon_history(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
    limit: int = 30
):
    """Get user's carbon footprint history"""
    try:
        carbon_logs = db.query(CarbonLog).filter(
            CarbonLog.user_id == current_user.id
        ).order_by(CarbonLog.date.desc()).limit(limit).all()
        
        history = []
        for log in carbon_logs:
            history.append({
                "id": log.id,
                "date": log.date.isoformat(),
                "daily_footprint_kg_co2": log.daily_footprint_kg_co2,
                "annual_estimate_tons_co2": log.annual_estimate_tons_co2,
                "transportation_data": log.transportation_data,
                "energy_data": log.energy_data,
                "consumption_data": log.consumption_data,
                "location": log.location,
                "notes": log.notes
            })
        
        return {
            "status": "success",
            "history": history,
            "total_logs": len(history),
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error("Error fetching carbon history", error=str(e), user_id=current_user.id)
        raise HTTPException(
            status_code=500,
            detail="Failed to fetch carbon history"
        )

@router.get("/stats")
async def get_carbon_stats(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get user's carbon footprint statistics"""
    try:
        from sqlalchemy import func
        
        # Get basic stats
        stats = db.query(
            func.count(CarbonLog.id).label('total_logs'),
            func.avg(CarbonLog.daily_footprint_kg_co2).label('avg_daily'),
            func.min(CarbonLog.daily_footprint_kg_co2).label('min_daily'),
            func.max(CarbonLog.daily_footprint_kg_co2).label('max_daily'),
            func.sum(CarbonLog.daily_footprint_kg_co2).label('total_co2')
        ).filter(CarbonLog.user_id == current_user.id).first()
        
        return {
            "status": "success",
            "stats": {
                "total_logs": stats.total_logs or 0,
                "average_daily_kg_co2": round(float(stats.avg_daily or 0), 2),
                "lowest_daily_kg_co2": round(float(stats.min_daily or 0), 2),
                "highest_daily_kg_co2": round(float(stats.max_daily or 0), 2),
                "total_tracked_kg_co2": round(float(stats.total_co2 or 0), 2),
                "estimated_annual_tons_co2": round(float(stats.avg_daily or 0) * 365 / 1000, 2)
            },
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error("Error fetching carbon stats", error=str(e), user_id=current_user.id)
        raise HTTPException(
            status_code=500,
            detail="Failed to fetch carbon statistics"
        )

@router.post("/activity", response_model=ActivityResponse)
async def log_activity(
    activity: ActivityRequest,
    current_user: Optional[User] = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Log a single activity and calculate its carbon footprint"""
    try:
        # Get emission factor
        factor = EMISSION_FACTORS.get(activity.activity_type.lower())
        if not factor:
            raise HTTPException(
                status_code=400,
                detail=f"Unknown activity type: {activity.activity_type}. Available types: {list(EMISSION_FACTORS.keys())}"
            )
        
        # Calculate emissions
        emissions = activity.value * factor
        
        # Determine unit based on activity type
        unit = activity.unit
        if not unit:
            if activity.activity_type.lower() in ["car", "bus", "train", "metro", "bike", "motorbike", "flight_domestic", "flight_international", "auto_rickshaw"]:
                unit = "km"
            elif activity.activity_type.lower() in ["beef", "lamb", "pork", "chicken", "fish", "vegetarian", "vegan", "dairy", "cheese"]:
                unit = "meal/serving"
            elif activity.activity_type.lower().startswith("electricity") or activity.activity_type.lower() in ["natural_gas"]:
                unit = "kWh"
            elif activity.activity_type.lower() in ["clothes_new", "clothes_secondhand", "smartphone", "laptop", "book", "plastic_bottle"]:
                unit = "item"
            elif activity.activity_type.lower() in ["paper_waste", "food_waste", "waste_general", "lpg_cooking"]:
                unit = "kg"
            elif activity.activity_type.lower() == "water_usage":
                unit = "liters"
            else:
                unit = "unit"
        
        # Generate suggestions based on activity type
        suggestions = get_activity_suggestions(activity.activity_type.lower(), emissions)
        
        # Determine category
        category = "other"
        if activity.activity_type.lower() in ["car", "car_diesel", "bus", "train", "metro", "bike", "motorbike", "flight_domestic", "flight_international", "auto_rickshaw"]:
            category = "transportation"
        elif activity.activity_type.lower() in ["beef", "lamb", "pork", "chicken", "fish", "vegetarian", "vegan", "dairy", "cheese"]:
            category = "food"
        elif activity.activity_type.lower().startswith("electricity") or activity.activity_type.lower() in ["natural_gas", "lpg_cooking", "water_heating"]:
            category = "energy"
        elif activity.activity_type.lower() in ["clothes_new", "clothes_secondhand", "smartphone", "laptop", "book", "plastic_bottle"]:
            category = "shopping"
        elif activity.activity_type.lower() in ["paper_waste", "food_waste", "waste_general", "water_usage"]:
            category = "household"
        
        # Save to database if user is authenticated
        if current_user:
            try:
                # Use the dedicated CarbonActivity table
                carbon_activity = CarbonActivity(
                    user_id=current_user.id,
                    date=datetime.utcnow(),
                    activity_type=activity.activity_type.lower(),
                    category=category,
                    value=activity.value,
                    unit=unit,
                    emissions_kg_co2=emissions,
                    emission_factor=factor,
                    description=activity.description,
                    is_shared=False  # Can be shared to social feed later
                )
                
                db.add(carbon_activity)
                db.commit()
                logger.info("Activity logged to database", 
                           user_id=current_user.id, 
                           activity=activity.activity_type,
                           emissions=emissions,
                           category=category)
            except Exception as e:
                logger.error("Failed to save activity log", error=str(e))
                # Don't fail the request if saving fails
        
        return ActivityResponse(
            activity_type=activity.activity_type,
            value=activity.value,
            unit=unit,
            emissions_kg_co2=round(emissions, 3),
            description=activity.description,
            timestamp=datetime.utcnow().isoformat(),
            suggestions=suggestions
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error logging activity", error=str(e))
        raise HTTPException(
            status_code=500,
            detail=f"Failed to log activity: {str(e)}"
        )

@router.get("/activities")
async def get_available_activities():
    """Get list of available activity types and their emission factors"""
    activities = {}
    
    for activity_type, factor in EMISSION_FACTORS.items():
        category = "transportation"
        unit = "km"
        
        if activity_type in ["beef", "lamb", "pork", "chicken", "fish", "vegetarian", "vegan", "dairy", "cheese"]:
            category = "food"
            unit = "meal/serving"
        elif activity_type.startswith("electricity") or activity_type in ["natural_gas"]:
            category = "energy"
            unit = "kWh"
        elif activity_type in ["clothes_new", "clothes_secondhand", "smartphone", "laptop", "book", "plastic_bottle"]:
            category = "shopping"
            unit = "item"
        elif activity_type in ["paper_waste", "food_waste", "waste_general", "lpg_cooking"]:
            category = "household"
            unit = "kg"
        elif activity_type == "water_usage":
            category = "household"
            unit = "liters"
        elif activity_type == "water_heating":
            category = "energy"
            unit = "usage"
        
        activities[activity_type] = {
            "category": category,
            "emission_factor": factor,
            "unit": unit,
            "description": get_activity_description(activity_type)
        }
    
    return {
        "status": "success",
        "activities": activities,
        "categories": {
            "transportation": "🚗 Transport (car, bike, bus, flight)",
            "food": "🍔 Food (meat, vegetarian, vegan, dairy)",
            "energy": "⚡ Energy (electricity, gas, water heating)",
            "shopping": "🛍️ Shopping (clothes, electronics, books)",
            "household": "🏠 Household (waste, water usage)"
        }
    }

def get_activity_suggestions(activity_type: str, emissions: float) -> list[str]:
    """Get personalized suggestions based on activity type and emissions"""
    suggestions = []
    
    if activity_type == "car":
        suggestions = [
            f"🚌 Taking the bus would reduce emissions by ~{emissions * 0.6:.1f} kg CO₂",
            f"🚆 Taking the train would reduce emissions by ~{emissions * 0.67:.1f} kg CO₂",
            f"🚴 Cycling would eliminate all {emissions:.1f} kg CO₂ from this trip",
            "🚗 Consider carpooling to share emissions with others"
        ]
    elif activity_type == "beef":
        suggestions = [
            f"🐔 Choosing chicken instead would save ~{emissions - 1.5:.1f} kg CO₂",
            f"🥗 A vegetarian meal would save ~{emissions - 0.8:.1f} kg CO₂",
            f"🌱 A vegan meal would save ~{emissions - 0.5:.1f} kg CO₂",
            "🌍 Reducing beef consumption once a week saves ~260 kg CO₂ annually"
        ]
    elif activity_type == "electricity_india":
        suggestions = [
            "💡 Switch to LED bulbs to reduce electricity consumption",
            "🌞 Consider solar panels for renewable energy",
            "❄️ Set AC temperature to 24°C or higher to save energy",
            "🔌 Unplug devices when not in use to reduce standby power"
        ]
    elif activity_type == "flight_domestic":
        suggestions = [
            f"🚆 Train travel would reduce emissions by ~{emissions * 0.84:.1f} kg CO₂",
            "📹 Consider video conferencing for business meetings",
            "🌳 Offset your flight emissions by planting trees",
            "✈️ Choose direct flights when possible (more efficient)"
        ]
    elif activity_type in ["clothes_new"]:
        suggestions = [
            f"👕 Buying secondhand would save ~{emissions - 2:.1f} kg CO₂",
            "♻️ Donate or recycle old clothes instead of throwing away",
            "🧵 Choose quality items that last longer",
            "🌱 Look for sustainable fashion brands"
        ]
    else:
        suggestions = [
            f"🌱 Great job tracking! You generated {emissions:.1f} kg CO₂ from this activity",
            "📊 Keep logging activities to understand your carbon footprint",
            "🎯 Small changes in daily habits can make a big difference",
            "🌍 Every action counts towards fighting climate change"
        ]
    
    return suggestions[:3]  # Return top 3 suggestions

def get_activity_description(activity_type: str) -> str:
    """Get human-readable description for activity type"""
    descriptions = {
        "car": "Petrol car travel",
        "car_diesel": "Diesel car travel", 
        "bus": "Public bus travel",
        "train": "Train travel",
        "metro": "Metro/subway travel",
        "bike": "Bicycle (zero emissions)",
        "motorbike": "Motorcycle travel",
        "flight_domestic": "Domestic flight",
        "flight_international": "International flight",
        "auto_rickshaw": "Auto-rickshaw travel",
        "beef": "Beef meal",
        "lamb": "Lamb meal",
        "pork": "Pork meal", 
        "chicken": "Chicken meal",
        "fish": "Fish meal",
        "vegetarian": "Vegetarian meal",
        "vegan": "Vegan meal",
        "dairy": "Dairy (milk, yogurt)",
        "cheese": "Cheese serving",
        "electricity_india": "Grid electricity (India)",
        "electricity_renewable": "Renewable electricity",
        "natural_gas": "Natural gas usage",
        "lpg_cooking": "LPG cooking gas",
        "water_heating": "Water heating",
        "clothes_new": "New clothing item",
        "clothes_secondhand": "Secondhand clothing",
        "smartphone": "New smartphone",
        "laptop": "New laptop",
        "book": "Book purchase",
        "plastic_bottle": "Plastic bottle",
        "paper_waste": "Paper waste",
        "food_waste": "Food waste",
        "waste_general": "General waste",
        "water_usage": "Water consumption"
    }
    return descriptions.get(activity_type, activity_type.replace("_", " ").title())

@router.get("/recent-activities")
async def get_recent_activities(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
    limit: int = 20
):
    """Get user's recent carbon activities"""
    try:
        activities = db.query(CarbonActivity).filter(
            CarbonActivity.user_id == current_user.id
        ).order_by(CarbonActivity.date.desc()).limit(limit).all()
        
        recent_activities = []
        for activity in activities:
            recent_activities.append({
                "id": activity.id,
                "date": activity.date.isoformat(),
                "activity_type": activity.activity_type,
                "category": activity.category,
                "value": activity.value,
                "unit": activity.unit,
                "emissions_kg_co2": activity.emissions_kg_co2,
                "emission_factor": activity.emission_factor,
                "description": activity.description,
                "is_shared": activity.is_shared
            })
        
        return {
            "status": "success",
            "activities": recent_activities,
            "total_activities": len(recent_activities),
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error("Error fetching recent activities", error=str(e), user_id=current_user.id)
        raise HTTPException(
            status_code=500,
            detail="Failed to fetch recent activities"
        )

@router.get("/dashboard")
async def get_carbon_dashboard(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get comprehensive carbon dashboard data"""
    try:
        from sqlalchemy import func, desc
        from datetime import timedelta
        
        # Get activity stats by category (last 30 days)
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        
        category_stats = db.query(
            CarbonActivity.category,
            func.sum(CarbonActivity.emissions_kg_co2).label('total_emissions'),
            func.count(CarbonActivity.id).label('activity_count'),
            func.avg(CarbonActivity.emissions_kg_co2).label('avg_emissions')
        ).filter(
            CarbonActivity.user_id == current_user.id,
            CarbonActivity.date >= thirty_days_ago
        ).group_by(CarbonActivity.category).all()
        
        # Get daily emissions for the last 7 days
        seven_days_ago = datetime.utcnow() - timedelta(days=7)
        daily_emissions = db.query(
            func.date(CarbonActivity.date).label('date'),
            func.sum(CarbonActivity.emissions_kg_co2).label('total_emissions')
        ).filter(
            CarbonActivity.user_id == current_user.id,
            CarbonActivity.date >= seven_days_ago
        ).group_by(func.date(CarbonActivity.date)).order_by(desc('date')).all()
        
        # Get top emission activities
        top_activities = db.query(
            CarbonActivity.activity_type,
            func.sum(CarbonActivity.emissions_kg_co2).label('total_emissions'),
            func.count(CarbonActivity.id).label('count')
        ).filter(
            CarbonActivity.user_id == current_user.id,
            CarbonActivity.date >= thirty_days_ago
        ).group_by(CarbonActivity.activity_type).order_by(desc('total_emissions')).limit(5).all()
        
        # Calculate totals
        total_emissions_30d = sum([stat.total_emissions for stat in category_stats])
        total_activities_30d = sum([stat.activity_count for stat in category_stats])
        
        # Prepare response data
        category_breakdown = {}
        for stat in category_stats:
            category_breakdown[stat.category] = {
                "total_emissions_kg_co2": round(float(stat.total_emissions), 2),
                "activity_count": stat.activity_count,
                "average_emissions_kg_co2": round(float(stat.avg_emissions), 2),
                "percentage": round((float(stat.total_emissions) / total_emissions_30d * 100), 1) if total_emissions_30d > 0 else 0
            }
        
        daily_data = [
            {
                "date": str(day.date),
                "emissions_kg_co2": round(float(day.total_emissions), 2)
            } for day in daily_emissions
        ]
        
        top_activities_data = [
            {
                "activity_type": activity.activity_type,
                "total_emissions_kg_co2": round(float(activity.total_emissions), 2),
                "activity_count": activity.count,
                "description": get_activity_description(activity.activity_type)
            } for activity in top_activities
        ]
        
        # Compare to averages (rough estimates for India)
        daily_avg_india = 6.8  # kg CO₂ per day average for India
        user_daily_avg = total_emissions_30d / 30 if total_emissions_30d > 0 else 0
        comparison_percentage = ((user_daily_avg - daily_avg_india) / daily_avg_india * 100) if daily_avg_india > 0 else 0
        
        return {
            "status": "success",
            "summary": {
                "total_emissions_30d_kg_co2": round(total_emissions_30d, 2),
                "total_activities_30d": total_activities_30d,
                "daily_average_kg_co2": round(user_daily_avg, 2),
                "annual_estimate_tons_co2": round(user_daily_avg * 365 / 1000, 2),
                "comparison_to_india_avg": {
                    "percentage_difference": round(comparison_percentage, 1),
                    "status": "below" if comparison_percentage < 0 else "above",
                    "india_daily_avg_kg_co2": daily_avg_india
                }
            },
            "category_breakdown": category_breakdown,
            "daily_emissions_7d": daily_data,
            "top_activities": top_activities_data,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error("Error fetching carbon dashboard", error=str(e), user_id=current_user.id)
        raise HTTPException(
            status_code=500,
            detail="Failed to fetch carbon dashboard data"
        )
