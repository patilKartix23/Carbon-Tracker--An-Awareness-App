"""
Climate data API routes (FastAPI version)
"""
from fastapi import APIRouter, HTTPException, Query, Depends
from typing import Optional
import structlog
from datetime import datetime, timedelta

from services.data_integrator import ClimateDataIntegrator
from api.auth import get_current_active_user
from database.models import User

logger = structlog.get_logger()
router = APIRouter()
data_integrator = ClimateDataIntegrator()

@router.get("/data")
async def get_climate_data(
    lat: float = Query(..., ge=-90, le=90, description="Latitude"),
    lon: float = Query(..., ge=-180, le=180, description="Longitude"),
    days: int = Query(7, ge=1, le=30, description="Number of days of historical data"),
    current_user: Optional[User] = Depends(get_current_active_user)
):
    """Get comprehensive climate data for a location"""
    try:
        # Calculate date range
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        # Format dates for NASA API
        start_str = start_date.strftime('%Y-%m-%d')
        end_str = end_date.strftime('%Y-%m-%d')
        
        # Fetch data from multiple sources
        nasa_data = await data_integrator.get_nasa_satellite_data(lat, lon, start_str, end_str)
        air_quality = await data_integrator.get_air_quality_data(lat, lon)
        weather_forecast = await data_integrator.get_weather_forecast(lat, lon)
        current_weather = await data_integrator.get_current_weather(lat, lon)
        
        # Process and combine data
        processed_data = data_integrator.process_and_normalize_data(nasa_data)
        
        logger.info("Climate data fetched successfully", 
                   lat=lat, lon=lon, days=days,
                   user_id=current_user.id if current_user else None)
        
        return {
            "status": "success",
            "location": {"lat": lat, "lon": lon},
            "date_range": {"start": start_str, "end": end_str},
            "data": {
                "current_weather": current_weather,
                "historical_climate": nasa_data,
                "air_quality": air_quality,
                "weather_forecast": weather_forecast,
                "processed_summary": processed_data.to_dict() if not processed_data.empty else {}
            },
            "timestamp": datetime.utcnow().isoformat()
        }
    
    except Exception as e:
        logger.error("Error fetching climate data", error=str(e), lat=lat, lon=lon)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch climate data: {str(e)}"
        )

@router.get("/air-quality")
async def get_air_quality(
    lat: float = Query(..., ge=-90, le=90, description="Latitude"),
    lon: float = Query(..., ge=-180, le=180, description="Longitude"),
    current_user: Optional[User] = Depends(get_current_active_user)
):
    """Get current air quality data for a location"""
    try:
        air_quality_data = await data_integrator.get_air_quality_data(lat, lon)
        
        logger.info("Air quality data fetched", 
                   lat=lat, lon=lon,
                   user_id=current_user.id if current_user else None)
        
        return {
            "status": "success",
            "location": {"lat": lat, "lon": lon},
            "air_quality": air_quality_data,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    except Exception as e:
        logger.error("Error fetching air quality", error=str(e), lat=lat, lon=lon)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch air quality data: {str(e)}"
        )

@router.get("/weather-forecast")
async def get_weather_forecast(
    lat: float = Query(..., ge=-90, le=90, description="Latitude"),
    lon: float = Query(..., ge=-180, le=180, description="Longitude"),
    current_user: Optional[User] = Depends(get_current_active_user)
):
    """Get weather forecast for a location"""
    try:
        forecast_data = await data_integrator.get_weather_forecast(lat, lon)
        
        logger.info("Weather forecast fetched", 
                   lat=lat, lon=lon,
                   user_id=current_user.id if current_user else None)
        
        return {
            "status": "success",
            "location": {"lat": lat, "lon": lon},
            "forecast": forecast_data,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    except Exception as e:
        logger.error("Error fetching weather forecast", error=str(e), lat=lat, lon=lon)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch weather forecast: {str(e)}"
        )

@router.get("/current-weather")
async def get_current_weather(
    lat: float = Query(..., ge=-90, le=90, description="Latitude"),
    lon: float = Query(..., ge=-180, le=180, description="Longitude"),
    current_user: Optional[User] = Depends(get_current_active_user)
):
    """Get current weather for a location"""
    try:
        weather_data = await data_integrator.get_current_weather(lat, lon)
        
        logger.info("Current weather fetched", 
                   lat=lat, lon=lon,
                   city=weather_data.get('name', 'Unknown'),
                   user_id=current_user.id if current_user else None)
        
        return {
            "status": "success",
            "location": {"lat": lat, "lon": lon},
            "weather": weather_data,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    except Exception as e:
        logger.error("Error fetching current weather", error=str(e), lat=lat, lon=lon)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch current weather: {str(e)}"
        )

@router.get("/bengaluru")
async def get_bengaluru_weather(current_user: Optional[User] = Depends(get_current_active_user)):
    """Get current weather for Bengaluru (Bangalore), India"""
    # Bengaluru coordinates
    lat, lon = 12.9716, 77.5946
    
    try:
        weather_data = await data_integrator.get_current_weather(lat, lon)
        air_quality_data = await data_integrator.get_air_quality_data(lat, lon)
        
        logger.info("Bengaluru weather fetched", 
                   user_id=current_user.id if current_user else None)
        
        return {
            "status": "success",
            "city": "Bengaluru",
            "location": {"lat": lat, "lon": lon},
            "weather": weather_data,
            "air_quality": air_quality_data,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    except Exception as e:
        logger.error("Error fetching Bengaluru weather", error=str(e))
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch Bengaluru weather: {str(e)}"
        )

@router.get("/mumbai")
async def get_mumbai_weather(current_user: Optional[User] = Depends(get_current_active_user)):
    """Get current weather for Mumbai, India"""
    lat, lon = 19.0760, 72.8777
    
    try:
        weather_data = await data_integrator.get_current_weather(lat, lon)
        air_quality_data = await data_integrator.get_air_quality_data(lat, lon)
        
        logger.info("Mumbai weather fetched", user_id=current_user.id if current_user else None)
        
        return {
            "status": "success",
            "city": "Mumbai",
            "location": {"lat": lat, "lon": lon},
            "weather": weather_data,
            "air_quality": air_quality_data,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    except Exception as e:
        logger.error("Error fetching Mumbai weather", error=str(e))
        raise HTTPException(status_code=500, detail=f"Failed to fetch Mumbai weather: {str(e)}")

@router.get("/delhi")
async def get_delhi_weather(current_user: Optional[User] = Depends(get_current_active_user)):
    """Get current weather for New Delhi, India"""
    lat, lon = 28.6139, 77.2090
    
    try:
        weather_data = await data_integrator.get_current_weather(lat, lon)
        air_quality_data = await data_integrator.get_air_quality_data(lat, lon)
        
        logger.info("Delhi weather fetched", user_id=current_user.id if current_user else None)
        
        return {
            "status": "success",
            "city": "New Delhi",
            "location": {"lat": lat, "lon": lon},
            "weather": weather_data,
            "air_quality": air_quality_data,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    except Exception as e:
        logger.error("Error fetching Delhi weather", error=str(e))
        raise HTTPException(status_code=500, detail=f"Failed to fetch Delhi weather: {str(e)}")

@router.get("/kolkata")
async def get_kolkata_weather(current_user: Optional[User] = Depends(get_current_active_user)):
    """Get current weather for Kolkata, India"""
    lat, lon = 22.5726, 88.3639
    
    try:
        weather_data = await data_integrator.get_current_weather(lat, lon)
        air_quality_data = await data_integrator.get_air_quality_data(lat, lon)
        
        logger.info("Kolkata weather fetched", user_id=current_user.id if current_user else None)
        
        return {
            "status": "success",
            "city": "Kolkata",
            "location": {"lat": lat, "lon": lon},
            "weather": weather_data,
            "air_quality": air_quality_data,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    except Exception as e:
        logger.error("Error fetching Kolkata weather", error=str(e))
        raise HTTPException(status_code=500, detail=f"Failed to fetch Kolkata weather: {str(e)}")

@router.get("/chennai")
async def get_chennai_weather(current_user: Optional[User] = Depends(get_current_active_user)):
    """Get current weather for Chennai, India"""
    lat, lon = 13.0827, 80.2707
    
    try:
        weather_data = await data_integrator.get_current_weather(lat, lon)
        air_quality_data = await data_integrator.get_air_quality_data(lat, lon)
        
        logger.info("Chennai weather fetched", user_id=current_user.id if current_user else None)
        
        return {
            "status": "success",
            "city": "Chennai",
            "location": {"lat": lat, "lon": lon},
            "weather": weather_data,
            "air_quality": air_quality_data,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    except Exception as e:
        logger.error("Error fetching Chennai weather", error=str(e))
        raise HTTPException(status_code=500, detail=f"Failed to fetch Chennai weather: {str(e)}")

@router.get("/hyderabad")
async def get_hyderabad_weather(current_user: Optional[User] = Depends(get_current_active_user)):
    """Get current weather for Hyderabad, India"""
    lat, lon = 17.3850, 78.4867
    
    try:
        weather_data = await data_integrator.get_current_weather(lat, lon)
        air_quality_data = await data_integrator.get_air_quality_data(lat, lon)
        
        logger.info("Hyderabad weather fetched", user_id=current_user.id if current_user else None)
        
        return {
            "status": "success",
            "city": "Hyderabad",
            "location": {"lat": lat, "lon": lon},
            "weather": weather_data,
            "air_quality": air_quality_data,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    except Exception as e:
        logger.error("Error fetching Hyderabad weather", error=str(e))
        raise HTTPException(status_code=500, detail=f"Failed to fetch Hyderabad weather: {str(e)}")

@router.get("/alerts")
async def get_climate_alerts(
    lat: float = Query(..., ge=-90, le=90, description="Latitude"),
    lon: float = Query(..., ge=-180, le=180, description="Longitude"),
    current_user: User = Depends(get_current_active_user)
):
    """Get climate alerts and warnings for a location"""
    try:
        # Get current conditions
        air_quality = await data_integrator.get_air_quality_data(lat, lon)
        weather_forecast = await data_integrator.get_weather_forecast(lat, lon)
        
        alerts = []
        
        # Air quality alerts
        if air_quality and 'aqi' in air_quality:
            aqi = air_quality['aqi']
            if aqi > 150:
                alerts.append({
                    "type": "air_quality",
                    "severity": "high" if aqi > 200 else "moderate",
                    "title": "Poor Air Quality Alert",
                    "message": f"AQI is {aqi}. Consider limiting outdoor activities.",
                    "timestamp": datetime.utcnow().isoformat()
                })
        
        # Weather alerts (simplified example)
        if weather_forecast and 'current' in weather_forecast:
            temp = weather_forecast['current'].get('temp', 0)
            if temp > 35:  # 35°C = ~95°F
                alerts.append({
                    "type": "extreme_heat",
                    "severity": "high",
                    "title": "Extreme Heat Warning",
                    "message": f"Temperature is {temp}°C. Stay hydrated and avoid prolonged sun exposure.",
                    "timestamp": datetime.utcnow().isoformat()
                })
        
        return {
            "status": "success",
            "location": {"lat": lat, "lon": lon},
            "alerts": alerts,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error("Error fetching climate alerts", error=str(e), lat=lat, lon=lon)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch climate alerts: {str(e)}"
        )
