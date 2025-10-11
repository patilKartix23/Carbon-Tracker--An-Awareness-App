"""
Machine Learning API routes - Forecasting and Image Analysis
"""
from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import structlog
from datetime import datetime, timedelta
import numpy as np
import cv2
import io
from PIL import Image

from api.auth import get_current_active_user
from database.models import User
from services.ml_service import MLService
from core.config import settings

logger = structlog.get_logger()
router = APIRouter()

# Initialize ML service
ml_service = MLService() if settings.ENABLE_ML_FEATURES else None

class ForecastRequest(BaseModel):
    """Weather/AQI forecast request"""
    latitude: float
    longitude: float
    days: int = 7
    features: List[str] = ["temperature", "aqi", "humidity"]

class ImageAnalysisResponse(BaseModel):
    """Image analysis response"""
    status: str
    analysis: Dict[str, Any]
    confidence_scores: Dict[str, float]
    detected_objects: List[Dict[str, Any]]
    environmental_score: Optional[float] = None

@router.post("/forecast")
async def get_ml_forecast(
    request: ForecastRequest,
    current_user: User = Depends(get_current_active_user)
):
    """Get ML-based climate forecasts"""
    try:
        if not ml_service:
            # Return mock data when ML is disabled
            mock_forecast = {
                "predictions": [
                    {
                        "date": (datetime.utcnow().date() + timedelta(days=i)).isoformat(),
                        "temperature": 20 + np.random.normal(0, 5),
                        "aqi": max(50, 100 + np.random.normal(0, 30)),
                        "humidity": max(30, min(90, 60 + np.random.normal(0, 15)))
                    }
                    for i in range(1, request.days + 1)
                ],
                "model_info": {
                    "name": "mock_model",
                    "accuracy": 0.85,
                    "last_trained": "2024-01-01T00:00:00Z"
                },
                "confidence_interval": {
                    "lower_bound": 0.8,
                    "upper_bound": 0.95
                }
            }
            
            return {
                "status": "success",
                "location": {"lat": request.latitude, "lon": request.longitude},
                "forecast": mock_forecast,
                "features": request.features,
                "timestamp": datetime.utcnow().isoformat(),
                "note": "Mock forecast data (enable ML features for real predictions)"
            }
        
        # Real ML prediction
        forecast_data = await ml_service.predict_climate(
            latitude=request.latitude,
            longitude=request.longitude,
            days=request.days,
            features=request.features
        )
        
        logger.info("ML forecast generated", 
                   user_id=current_user.id,
                   lat=request.latitude, 
                   lon=request.longitude,
                   days=request.days)
        
        return {
            "status": "success",
            "location": {"lat": request.latitude, "lon": request.longitude},
            "forecast": forecast_data,
            "features": request.features,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error("ML forecast failed", error=str(e), user_id=current_user.id)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate forecast: {str(e)}"
        )

@router.post("/analyze-image", response_model=ImageAnalysisResponse)
async def analyze_image(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_active_user)
):
    """Analyze uploaded image for environmental content"""
    try:
        # Validate image
        if not file.content_type.startswith('image/'):
            raise HTTPException(
                status_code=400,
                detail="File must be an image"
            )
        
        # Read image
        image_data = await file.read()
        
        if not ml_service:
            # Return mock analysis
            mock_analysis = {
                "detected_objects": [
                    {"object": "tree", "confidence": 0.92, "bbox": [100, 100, 200, 300]},
                    {"object": "sky", "confidence": 0.88, "bbox": [0, 0, 800, 200]},
                    {"object": "grass", "confidence": 0.75, "bbox": [0, 300, 800, 400]}
                ],
                "environmental_features": {
                    "vegetation_coverage": 0.65,
                    "air_quality_indicators": {
                        "visibility": "good",
                        "sky_clarity": 0.8
                    },
                    "urban_vs_natural": "natural_dominant"
                },
                "sustainability_score": 8.2,
                "recommendations": [
                    "Great natural environment! Consider sharing this location with others.",
                    "This area shows good air quality based on visibility."
                ]
            }
            
            return ImageAnalysisResponse(
                status="success",
                analysis=mock_analysis,
                confidence_scores={
                    "overall": 0.85,
                    "environmental": 0.82,
                    "object_detection": 0.88
                },
                detected_objects=mock_analysis["detected_objects"],
                environmental_score=mock_analysis["sustainability_score"]
            )
        
        # Real ML image analysis
        analysis_result = await ml_service.analyze_environmental_image(image_data)
        
        logger.info("Image analysis completed", 
                   user_id=current_user.id,
                   filename=file.filename,
                   detected_objects=len(analysis_result.get("detected_objects", [])))
        
        return ImageAnalysisResponse(
            status="success",
            analysis=analysis_result,
            confidence_scores=analysis_result.get("confidence_scores", {}),
            detected_objects=analysis_result.get("detected_objects", []),
            environmental_score=analysis_result.get("environmental_score")
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Image analysis failed", error=str(e), user_id=current_user.id)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to analyze image: {str(e)}"
        )

@router.get("/recommendations")
async def get_personalized_recommendations(
    current_user: User = Depends(get_current_active_user),
    location: Optional[str] = None,
    category: Optional[str] = None
):
    """Get personalized environmental recommendations"""
    try:
        if not ml_service:
            # Return mock recommendations
            mock_recommendations = {
                "daily_tips": [
                    {
                        "category": "transportation",
                        "tip": "Consider biking or walking for trips under 2 miles",
                        "impact": "Save 2.3 kg CO2 per day",
                        "difficulty": "easy"
                    },
                    {
                        "category": "energy",
                        "tip": "Adjust thermostat by 2°C when away from home",
                        "impact": "Save 1.8 kg CO2 per day",
                        "difficulty": "easy"
                    }
                ],
                "weekly_challenges": [
                    {
                        "title": "Meatless Monday",
                        "description": "Try plant-based meals one day this week",
                        "potential_impact": "Save 6.1 kg CO2",
                        "category": "diet"
                    }
                ],
                "location_specific": [
                    {
                        "tip": f"Local air quality is good in {location or 'your area'} - great day for outdoor activities!",
                        "category": "health"
                    }
                ] if location else []
            }
            
            return {
                "status": "success",
                "recommendations": mock_recommendations,
                "personalization_factors": {
                    "user_history": "limited_data",
                    "location": location or "not_provided",
                    "preferences": "default"
                },
                "timestamp": datetime.utcnow().isoformat(),
                "note": "Mock recommendations (enable ML for personalized suggestions)"
            }
        
        # Real ML recommendations
        recommendations = await ml_service.get_personalized_recommendations(
            user_id=current_user.id,
            location=location,
            category=category
        )
        
        logger.info("Personalized recommendations generated", 
                   user_id=current_user.id,
                   location=location,
                   category=category)
        
        return {
            "status": "success",
            "recommendations": recommendations,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error("Recommendations generation failed", error=str(e), user_id=current_user.id)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate recommendations: {str(e)}"
        )

@router.get("/models/status")
async def get_model_status(current_user: User = Depends(get_current_active_user)):
    """Get status of ML models"""
    try:
        if not ml_service:
            return {
                "status": "disabled",
                "message": "ML features are disabled",
                "models": {},
                "timestamp": datetime.utcnow().isoformat()
            }
        
        model_status = await ml_service.get_model_status()
        
        return {
            "status": "active",
            "models": model_status,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error("Model status check failed", error=str(e))
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get model status: {str(e)}"
        )
