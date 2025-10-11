import aiohttp
import asyncio
import pandas as pd
from typing import Dict, List, Optional
import os
from datetime import datetime, timedelta
import json
import structlog

logger = structlog.get_logger()

class ClimateDataIntegrator:
    def __init__(self):
        self.nasa_api_key = os.getenv('NASA_API_KEY')
        self.noaa_api_key = os.getenv('NOAA_API_KEY')
        self.openweather_api_key = os.getenv('OPENWEATHER_API_KEY')
        
    async def get_nasa_satellite_data(self, lat: float, lon: float, start_date: str, end_date: str) -> Dict:
        """Fetch NASA satellite data for given coordinates and date range"""
        base_url = "https://power.larc.nasa.gov/api/temporal/daily/point"
        
        params = {
            'parameters': 'T2M,PRECTOTCORR,WS2M,RH2M',  # Temperature, Precipitation, Wind Speed, Humidity
            'community': 'AG',
            'longitude': lon,
            'latitude': lat,
            'start': start_date.replace('-', ''),
            'end': end_date.replace('-', ''),
            'format': 'JSON'
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(base_url, params=params, timeout=30) as response:
                    response.raise_for_status()
                    return await response.json()
        except Exception as e:
            logger.error("Error fetching NASA data", error=str(e))
            # Return mock data for development
            return self.get_mock_nasa_data()
    
    async def get_air_quality_data(self, lat: float, lon: float) -> Dict:
        """Fetch air quality data from OpenWeatherMap API"""
        if not self.openweather_api_key:
            logger.warning("No OpenWeatherMap API key, using mock data")
            return self.get_mock_air_quality_data()
            
        base_url = f"http://api.openweathermap.org/data/2.5/air_pollution"
        
        params = {
            'lat': lat,
            'lon': lon,
            'appid': self.openweather_api_key
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(base_url, params=params, timeout=10) as response:
                    response.raise_for_status()
                    data = await response.json()
                    logger.info("Successfully fetched real air quality data", lat=lat, lon=lon)
                    return data
        except Exception as e:
            logger.error("Error fetching air quality data, using mock", error=str(e))
            return self.get_mock_air_quality_data()
    
    async def get_weather_forecast(self, lat: float, lon: float) -> Dict:
        """Fetch weather forecast data"""
        if not self.openweather_api_key:
            logger.warning("No OpenWeatherMap API key, using mock data")
            return self.get_mock_weather_data()
            
        base_url = f"http://api.openweathermap.org/data/2.5/forecast"
        
        params = {
            'lat': lat,
            'lon': lon,
            'appid': self.openweather_api_key,
            'units': 'metric'
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(base_url, params=params, timeout=10) as response:
                    response.raise_for_status()
                    data = await response.json()
                    logger.info("Successfully fetched real weather data", lat=lat, lon=lon)
                    return data
        except Exception as e:
            logger.error("Error fetching weather forecast, using mock", error=str(e))
            return self.get_mock_weather_data()

    async def get_current_weather(self, lat: float, lon: float) -> Dict:
        """Fetch current weather data"""
        if not self.openweather_api_key:
            logger.warning("No OpenWeatherMap API key, using mock data")
            return self.get_mock_current_weather()
            
        base_url = f"http://api.openweathermap.org/data/2.5/weather"
        
        params = {
            'lat': lat,
            'lon': lon,
            'appid': self.openweather_api_key,
            'units': 'metric'
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(base_url, params=params, timeout=10) as response:
                    response.raise_for_status()
                    data = await response.json()
                    logger.info("Successfully fetched current weather", lat=lat, lon=lon, city=data.get('name'))
                    return data
        except Exception as e:
            logger.error("Error fetching current weather, using mock", error=str(e))
            return self.get_mock_current_weather()
    
    def process_and_normalize_data(self, raw_data: Dict) -> pd.DataFrame:
        """Process and normalize different data sources"""
        processed_data = {}
        
        if 'properties' in raw_data and 'parameter' in raw_data['properties']:
            for param, values in raw_data['properties']['parameter'].items():
                processed_data[param] = list(values.values())
        
        return pd.DataFrame(processed_data)
    
    def get_mock_nasa_data(self) -> Dict:
        """Return mock NASA data for development/testing"""
        return {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [-74.0060, 40.7128, 0.0]
            },
            "properties": {
                "parameter": {
                    "T2M": {
                        "20250815": 22.5,
                        "20250816": 24.1,
                        "20250817": 23.8,
                        "20250818": 25.2,
                        "20250819": 26.1
                    },
                    "PRECTOTCORR": {
                        "20250815": 0.2,
                        "20250816": 0.0,
                        "20250817": 1.5,
                        "20250818": 0.0,
                        "20250819": 0.3
                    },
                    "WS2M": {
                        "20250815": 3.2,
                        "20250816": 2.8,
                        "20250817": 4.1,
                        "20250818": 2.5,
                        "20250819": 3.7
                    },
                    "RH2M": {
                        "20250815": 65.2,
                        "20250816": 58.7,
                        "20250817": 72.1,
                        "20250818": 61.3,
                        "20250819": 68.9
                    }
                }
            }
        }
    
    def get_mock_air_quality_data(self) -> Dict:
        """Return mock air quality data for development/testing"""
        return {
            "coord": {"lon": -74.0060, "lat": 40.7128},
            "list": [
                {
                    "main": {"aqi": 2},
                    "components": {
                        "co": 233.65,
                        "no": 0.01,
                        "no2": 0.65,
                        "o3": 268.46,
                        "so2": 0.36,
                        "pm2_5": 0.73,
                        "pm10": 0.82,
                        "nh3": 0.12
                    },
                    "dt": 1692453600
                }
            ]
        }
    
    def get_mock_weather_data(self) -> Dict:
        """Return mock weather data for development/testing"""
        return {
            "cod": "200",
            "message": 0,
            "cnt": 40,
            "list": [
                {
                    "dt": 1692453600,
                    "main": {
                        "temp": 24.5,
                        "feels_like": 26.2,
                        "temp_min": 22.1,
                        "temp_max": 26.8,
                        "pressure": 1013,
                        "humidity": 65
                    },
                    "weather": [
                        {
                            "id": 801,
                            "main": "Clouds",
                            "description": "few clouds",
                            "icon": "02d"
                        }
                    ],
                    "clouds": {"all": 20},
                    "wind": {"speed": 3.2, "deg": 230},
                    "visibility": 10000,
                    "pop": 0.1,
                    "dt_txt": "2025-08-19 12:00:00"
                }
            ]
        }

    def get_mock_current_weather(self) -> Dict:
        """Return mock current weather data for Bengaluru"""
        return {
            "coord": {"lon": 77.5946, "lat": 12.9716},
            "weather": [
                {
                    "id": 803,
                    "main": "Clouds",
                    "description": "broken clouds",
                    "icon": "04d"
                }
            ],
            "base": "stations",
            "main": {
                "temp": 28.5,
                "feels_like": 32.1,
                "temp_min": 26.8,
                "temp_max": 30.2,
                "pressure": 1013,
                "humidity": 68
            },
            "visibility": 6000,
            "wind": {
                "speed": 2.1,
                "deg": 240
            },
            "clouds": {
                "all": 75
            },
            "dt": 1692453600,
            "sys": {
                "type": 1,
                "id": 9205,
                "country": "IN",
                "sunrise": 1692406920,
                "sunset": 1692452340
            },
            "timezone": 19800,
            "id": 1277333,
            "name": "Bengaluru",
            "cod": 200
        }
