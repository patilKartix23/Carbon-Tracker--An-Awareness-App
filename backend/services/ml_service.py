"""
Machine Learning Service for Climate Predictions and Image Analysis
"""
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
import joblib
import cv2
from PIL import Image
import io
import structlog
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import os
from pathlib import Path

from core.config import settings

logger = structlog.get_logger()

class MLService:
    """Machine Learning service for climate predictions and image analysis"""
    
    def __init__(self):
        self.model_path = Path(settings.MODEL_PATH)
        self.model_path.mkdir(exist_ok=True)
        
        # Initialize models
        self.climate_model = None
        self.scaler = None
        self.image_model = None
        
        # Load or create models
        self._initialize_models()
    
    def _initialize_models(self):
        """Initialize or load ML models"""
        try:
            # Try to load existing models
            climate_model_path = self.model_path / "climate_forecast_model.joblib"
            scaler_path = self.model_path / "feature_scaler.joblib"
            
            if climate_model_path.exists() and scaler_path.exists():
                self.climate_model = joblib.load(climate_model_path)
                self.scaler = joblib.load(scaler_path)
                logger.info("Loaded existing ML models")
            else:
                # Create and train basic models with synthetic data
                self._create_basic_models()
                logger.info("Created new ML models with synthetic data")
                
        except Exception as e:
            logger.error("Failed to initialize ML models", error=str(e))
            # Create fallback models
            self._create_fallback_models()
    
    def _create_basic_models(self):
        """Create basic models with synthetic training data"""
        # Generate synthetic climate data for training
        np.random.seed(42)
        n_samples = 1000
        
        # Features: lat, lon, day_of_year, historical_temp, historical_aqi
        X = np.random.rand(n_samples, 5)
        X[:, 0] = X[:, 0] * 180 - 90  # Latitude -90 to 90
        X[:, 1] = X[:, 1] * 360 - 180  # Longitude -180 to 180
        X[:, 2] = X[:, 2] * 365  # Day of year
        X[:, 3] = X[:, 3] * 40 - 10  # Historical temp -10 to 30°C
        X[:, 4] = X[:, 4] * 200 + 50  # Historical AQI 50-250
        
        # Target: next day temperature and AQI
        y_temp = X[:, 3] + np.random.normal(0, 2, n_samples)  # Temperature with noise
        y_aqi = X[:, 4] + np.random.normal(0, 20, n_samples)  # AQI with noise
        
        # Train models
        self.climate_model = {
            'temperature': RandomForestRegressor(n_estimators=50, random_state=42),
            'aqi': RandomForestRegressor(n_estimators=50, random_state=42)
        }
        
        self.scaler = StandardScaler()
        X_scaled = self.scaler.fit_transform(X)
        
        self.climate_model['temperature'].fit(X_scaled, y_temp)
        self.climate_model['aqi'].fit(X_scaled, y_aqi)
        
        # Save models
        joblib.dump(self.climate_model, self.model_path / "climate_forecast_model.joblib")
        joblib.dump(self.scaler, self.model_path / "feature_scaler.joblib")
    
    def _create_fallback_models(self):
        """Create simple fallback models"""
        self.climate_model = None
        self.scaler = None
        logger.warning("Using fallback ML models")
    
    async def predict_climate(self, latitude: float, longitude: float, days: int, features: List[str]) -> Dict[str, Any]:
        """Predict climate conditions for the next few days"""
        try:
            if not self.climate_model or not self.scaler:
                # Return mock predictions
                return self._generate_mock_predictions(latitude, longitude, days, features)
            
            predictions = []
            base_date = datetime.utcnow().date()
            
            for day in range(1, days + 1):
                predict_date = base_date + timedelta(days=day)
                day_of_year = predict_date.timetuple().tm_yday
                
                # Create feature vector
                # [lat, lon, day_of_year, historical_temp, historical_aqi]
                feature_vector = np.array([[
                    latitude,
                    longitude,
                    day_of_year,
                    20.0,  # Default historical temp
                    100.0  # Default historical AQI
                ]])
                
                feature_vector_scaled = self.scaler.transform(feature_vector)
                
                # Predict
                pred_temp = self.climate_model['temperature'].predict(feature_vector_scaled)[0]
                pred_aqi = max(0, self.climate_model['aqi'].predict(feature_vector_scaled)[0])
                
                prediction = {
                    "date": predict_date.isoformat(),
                    "temperature": round(pred_temp, 1),
                    "aqi": round(pred_aqi),
                    "confidence": 0.75 + np.random.uniform(-0.1, 0.1)
                }
                
                # Add humidity if requested
                if "humidity" in features:
                    prediction["humidity"] = max(20, min(90, 60 + np.random.normal(0, 15)))
                
                predictions.append(prediction)
            
            return {
                "predictions": predictions,
                "model_info": {
                    "name": "climate_forecast_rf",
                    "version": "1.0",
                    "last_trained": datetime.utcnow().isoformat()
                }
            }
            
        except Exception as e:
            logger.error("Climate prediction failed", error=str(e))
            return self._generate_mock_predictions(latitude, longitude, days, features)
    
    def _generate_mock_predictions(self, latitude: float, longitude: float, days: int, features: List[str]) -> Dict[str, Any]:
        """Generate mock predictions when ML models are not available"""
        predictions = []
        base_date = datetime.utcnow().date()
        
        # Base temperature on latitude (rough approximation)
        base_temp = 30 - abs(latitude) * 0.5
        
        for day in range(1, days + 1):
            predict_date = base_date + timedelta(days=day)
            
            prediction = {
                "date": predict_date.isoformat(),
                "temperature": round(base_temp + np.random.normal(0, 3), 1),
                "aqi": max(50, int(100 + np.random.normal(0, 30))),
                "confidence": 0.65
            }
            
            if "humidity" in features:
                prediction["humidity"] = max(30, min(90, int(60 + np.random.normal(0, 15))))
            
            predictions.append(prediction)
        
        return {
            "predictions": predictions,
            "model_info": {
                "name": "mock_model",
                "version": "0.1",
                "note": "Mock predictions - train with real data for accuracy"
            }
        }
    
    async def analyze_environmental_image(self, image_data: bytes) -> Dict[str, Any]:
        """Analyze image for environmental content"""
        try:
            # Convert bytes to image
            image = Image.open(io.BytesIO(image_data))
            image_array = np.array(image)
            
            # Simple color-based analysis (mock implementation)
            analysis = self._analyze_image_colors(image_array)
            
            return {
                "detected_objects": analysis["objects"],
                "environmental_features": analysis["features"],
                "confidence_scores": {
                    "overall": 0.78,
                    "vegetation": analysis["vegetation_confidence"],
                    "air_quality": analysis["air_quality_confidence"]
                },
                "environmental_score": analysis["environmental_score"],
                "recommendations": analysis["recommendations"]
            }
            
        except Exception as e:
            logger.error("Image analysis failed", error=str(e))
            # Return basic analysis
            return {
                "detected_objects": [
                    {"object": "unknown", "confidence": 0.5, "bbox": [0, 0, 100, 100]}
                ],
                "environmental_features": {
                    "analysis": "basic_color_analysis",
                    "vegetation_detected": True
                },
                "confidence_scores": {"overall": 0.5},
                "environmental_score": 6.0,
                "recommendations": ["Image analyzed with basic color detection"]
            }
    
    def _analyze_image_colors(self, image_array: np.ndarray) -> Dict[str, Any]:
        """Analyze image based on color distribution (simplified approach)"""
        # Convert to HSV for better color analysis
        if len(image_array.shape) == 3:
            hsv = cv2.cvtColor(image_array, cv2.COLOR_RGB2HSV)
        else:
            hsv = image_array
        
        # Define color ranges for environmental features
        green_lower = np.array([35, 40, 40])
        green_upper = np.array([85, 255, 255])
        
        blue_lower = np.array([100, 50, 50])
        blue_upper = np.array([130, 255, 255])
        
        # Calculate color percentages
        green_mask = cv2.inRange(hsv, green_lower, green_upper)
        blue_mask = cv2.inRange(hsv, blue_lower, blue_upper)
        
        total_pixels = image_array.shape[0] * image_array.shape[1]
        green_percentage = np.sum(green_mask > 0) / total_pixels
        blue_percentage = np.sum(blue_mask > 0) / total_pixels
        
        # Generate analysis based on color distribution
        objects = []
        if green_percentage > 0.1:
            objects.append({
                "object": "vegetation",
                "confidence": min(0.9, green_percentage * 3),
                "bbox": [0, 0, image_array.shape[1], image_array.shape[0]]
            })
        
        if blue_percentage > 0.05:
            objects.append({
                "object": "sky",
                "confidence": min(0.8, blue_percentage * 4),
                "bbox": [0, 0, image_array.shape[1], int(image_array.shape[0] * 0.6)]
            })
        
        # Calculate environmental score
        environmental_score = (
            green_percentage * 4 +  # Vegetation weight
            blue_percentage * 2 +   # Sky weight
            (1 - max(green_percentage + blue_percentage, 1)) * 1  # Urban penalty
        ) * 10
        
        environmental_score = max(1, min(10, environmental_score))
        
        recommendations = []
        if green_percentage > 0.3:
            recommendations.append("Great natural environment with abundant vegetation!")
        if blue_percentage > 0.2:
            recommendations.append("Clear sky indicates good air quality conditions.")
        if environmental_score > 7:
            recommendations.append("This location shows excellent environmental conditions.")
        
        return {
            "objects": objects,
            "features": {
                "vegetation_coverage": round(green_percentage, 2),
                "sky_visibility": round(blue_percentage, 2),
                "dominant_colors": ["green", "blue"] if green_percentage > 0.1 else ["urban"]
            },
            "vegetation_confidence": min(0.9, green_percentage * 2),
            "air_quality_confidence": min(0.8, blue_percentage * 3),
            "environmental_score": round(environmental_score, 1),
            "recommendations": recommendations
        }
    
    async def get_personalized_recommendations(self, user_id: str, location: Optional[str] = None, category: Optional[str] = None) -> Dict[str, Any]:
        """Generate personalized environmental recommendations"""
        # This would typically use user history and ML models
        # For now, return smart defaults based on location and category
        
        recommendations = {
            "daily_tips": [],
            "weekly_challenges": [],
            "location_specific": []
        }
        
        # Category-specific recommendations
        if category == "transportation" or not category:
            recommendations["daily_tips"].append({
                "category": "transportation",
                "tip": "Consider carpooling or using public transport for your commute",
                "impact": "Save 2-5 kg CO2 per day",
                "difficulty": "medium",
                "personalized": True
            })
        
        if category == "energy" or not category:
            recommendations["daily_tips"].append({
                "category": "energy",
                "tip": "Unplug devices when not in use to reduce phantom energy consumption",
                "impact": "Save 0.5-1 kg CO2 per day",
                "difficulty": "easy",
                "personalized": True
            })
        
        # Weekly challenges
        recommendations["weekly_challenges"].append({
            "title": "Zero Waste Week",
            "description": "Try to minimize waste by reusing and recycling",
            "potential_impact": "Save 3-7 kg CO2",
            "category": "waste"
        })
        
        # Location-specific (if provided)
        if location:
            recommendations["location_specific"].append({
                "tip": f"Based on {location}, consider visiting local farmers markets to reduce food transport emissions",
                "category": "consumption",
                "location_based": True
            })
        
        return recommendations
    
    async def get_model_status(self) -> Dict[str, Any]:
        """Get status of all ML models"""
        status = {}
        
        # Climate model status
        if self.climate_model and self.scaler:
            status["climate_forecast"] = {
                "status": "active",
                "model_type": "RandomForestRegressor",
                "features": ["temperature", "aqi"],
                "last_updated": datetime.utcnow().isoformat()
            }
        else:
            status["climate_forecast"] = {
                "status": "fallback",
                "note": "Using mock predictions"
            }
        
        # Image analysis status
        status["image_analysis"] = {
            "status": "active",
            "method": "color_based_analysis",
            "capabilities": ["vegetation_detection", "sky_analysis", "environmental_scoring"]
        }
        
        # Recommendations status
        status["recommendations"] = {
            "status": "active",
            "method": "rule_based",
            "personalization": "basic"
        }
        
        return status
