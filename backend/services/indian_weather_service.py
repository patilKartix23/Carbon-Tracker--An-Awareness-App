import kagglehub
import pandas as pd
import numpy as np
import os
import json
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class IndianWeatherService:
    def __init__(self):
        self.dataset_path = None
        self.weather_data = None
        self.processed_data = {}
        self.indian_cities = self._get_indian_cities()
        
    def _get_indian_cities(self) -> Dict[str, Dict[str, float]]:
        """Major Indian cities with their coordinates"""
        return {
            'Mumbai': {'lat': 19.0760, 'lon': 72.8777, 'state': 'Maharashtra'},
            'Delhi': {'lat': 28.7041, 'lon': 77.1025, 'state': 'Delhi'},
            'Bangalore': {'lat': 12.9716, 'lon': 77.5946, 'state': 'Karnataka'},
            'Hyderabad': {'lat': 17.3850, 'lon': 78.4867, 'state': 'Telangana'},
            'Chennai': {'lat': 13.0827, 'lon': 80.2707, 'state': 'Tamil Nadu'},
            'Kolkata': {'lat': 22.5726, 'lon': 88.3639, 'state': 'West Bengal'},
            'Pune': {'lat': 18.5204, 'lon': 73.8567, 'state': 'Maharashtra'},
            'Ahmedabad': {'lat': 23.0225, 'lon': 72.5714, 'state': 'Gujarat'},
            'Jaipur': {'lat': 26.9124, 'lon': 75.7873, 'state': 'Rajasthan'},
            'Surat': {'lat': 21.1702, 'lon': 72.8311, 'state': 'Gujarat'},
            'Lucknow': {'lat': 26.8467, 'lon': 80.9462, 'state': 'Uttar Pradesh'},
            'Kanpur': {'lat': 26.4499, 'lon': 80.3319, 'state': 'Uttar Pradesh'},
            'Nagpur': {'lat': 21.1458, 'lon': 79.0882, 'state': 'Maharashtra'},
            'Indore': {'lat': 22.7196, 'lon': 75.8577, 'state': 'Madhya Pradesh'},
            'Thane': {'lat': 19.2183, 'lon': 72.9781, 'state': 'Maharashtra'},
            'Bhopal': {'lat': 23.2599, 'lon': 77.4126, 'state': 'Madhya Pradesh'},
            'Visakhapatnam': {'lat': 17.6868, 'lon': 83.2185, 'state': 'Andhra Pradesh'},
            'Patna': {'lat': 25.5941, 'lon': 85.1376, 'state': 'Bihar'},
            'Vadodara': {'lat': 22.3072, 'lon': 73.1812, 'state': 'Gujarat'},
            'Ghaziabad': {'lat': 28.6692, 'lon': 77.4538, 'state': 'Uttar Pradesh'}
        }
    
    def download_dataset(self) -> bool:
        """Download the Indian weather dataset from Kaggle"""
        try:
            logger.info("Downloading Indian weather dataset from Kaggle...")
            # Download latest version of the dataset
            self.dataset_path = kagglehub.dataset_download("pratikjadhav05/indian-weather-data")
            logger.info(f"Dataset downloaded to: {self.dataset_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to download dataset: {e}")
            # Use fallback mock data if download fails
            self._create_mock_data()
            return False
    
    def _create_mock_data(self):
        """Create mock Indian weather data for development/testing"""
        logger.info("Creating mock Indian weather data...")
        
        # Generate realistic weather data for Indian cities
        mock_data = []
        cities = list(self.indian_cities.keys())
        
        # Generate data for the last 365 days
        base_date = datetime.now() - timedelta(days=365)
        
        for i in range(365):
            current_date = base_date + timedelta(days=i)
            
            for city in cities[:10]:  # Use top 10 cities for mock data
                city_info = self.indian_cities[city]
                
                # Simulate seasonal weather patterns for India
                month = current_date.month
                
                # Temperature patterns (India has distinct seasons)
                if month in [12, 1, 2]:  # Winter
                    base_temp = np.random.normal(20, 5)  # 15-25°C
                elif month in [3, 4, 5]:  # Summer  
                    base_temp = np.random.normal(35, 8)  # 27-43°C
                elif month in [6, 7, 8, 9]:  # Monsoon
                    base_temp = np.random.normal(28, 5)  # 23-33°C
                else:  # Post-monsoon
                    base_temp = np.random.normal(25, 6)  # 19-31°C
                
                # Humidity patterns
                if month in [6, 7, 8, 9]:  # Monsoon - high humidity
                    humidity = np.random.normal(80, 10)
                else:
                    humidity = np.random.normal(60, 15)
                
                # Rainfall patterns
                if month in [6, 7, 8, 9]:  # Monsoon season
                    rainfall = np.random.exponential(5)  # Higher rainfall
                else:
                    rainfall = np.random.exponential(0.5)  # Lower rainfall
                
                mock_data.append({
                    'Date': current_date.strftime('%Y-%m-%d'),
                    'City': city,
                    'State': city_info['state'],
                    'Temperature': round(max(5, base_temp), 1),
                    'Humidity': round(max(20, min(100, humidity)), 1),
                    'Rainfall': round(max(0, rainfall), 2),
                    'Wind_Speed': round(np.random.normal(10, 5), 1),
                    'Pressure': round(np.random.normal(1013, 15), 1),
                    'Latitude': city_info['lat'],
                    'Longitude': city_info['lon']
                })
        
        self.weather_data = pd.DataFrame(mock_data)
        logger.info(f"Created mock dataset with {len(mock_data)} records")
    
    def load_and_process_data(self) -> bool:
        """Load and process the weather dataset"""
        try:
            if self.dataset_path and os.path.exists(self.dataset_path):
                # Try to find CSV files in the dataset
                csv_files = []
                for root, dirs, files in os.walk(self.dataset_path):
                    for file in files:
                        if file.endswith('.csv'):
                            csv_files.append(os.path.join(root, file))
                
                if csv_files:
                    logger.info(f"Found CSV files: {csv_files}")
                    # Load the first CSV file (assuming it's the main dataset)
                    self.weather_data = pd.read_csv(csv_files[0])
                    logger.info(f"Loaded dataset with {len(self.weather_data)} records")
                else:
                    logger.warning("No CSV files found in dataset, using mock data")
                    self._create_mock_data()
            else:
                logger.warning("Dataset path not found, using mock data")
                self._create_mock_data()
            
            # Process the data
            self._process_weather_data()
            return True
            
        except Exception as e:
            logger.error(f"Failed to load dataset: {e}")
            self._create_mock_data()
            self._process_weather_data()
            return False
    
    def _process_weather_data(self):
        """Process and aggregate weather data"""
        if self.weather_data is None:
            return
        
        try:
            # Convert date column if it exists
            if 'Date' in self.weather_data.columns:
                self.weather_data['Date'] = pd.to_datetime(self.weather_data['Date'])
            
            # Add month and year columns for aggregation
            if 'Date' in self.weather_data.columns:
                self.weather_data['Month'] = self.weather_data['Date'].dt.month
                self.weather_data['Year'] = self.weather_data['Date'].dt.year
            
            # Process data by city
            self.processed_data = {
                'cities_overview': self._get_cities_overview(),
                'monthly_trends': self._get_monthly_trends(),
                'current_conditions': self._get_current_conditions(),
                'regional_summary': self._get_regional_summary()
            }
            
            logger.info("Data processing completed successfully")
            
        except Exception as e:
            logger.error(f"Error processing data: {e}")
    
    def _get_cities_overview(self) -> List[Dict]:
        """Get overview data for all cities"""
        cities_data = []
        
        # Group by city and get latest data
        if 'City' in self.weather_data.columns:
            city_groups = self.weather_data.groupby('City')
            
            for city, group in city_groups:
                latest_data = group.iloc[-1]  # Get most recent record
                
                cities_data.append({
                    'city': city,
                    'state': latest_data.get('State', 'Unknown'),
                    'lat': latest_data.get('Latitude', self.indian_cities.get(city, {}).get('lat', 0)),
                    'lon': latest_data.get('Longitude', self.indian_cities.get(city, {}).get('lon', 0)),
                    'temperature': float(latest_data.get('Temperature', 0)),
                    'humidity': float(latest_data.get('Humidity', 0)),
                    'rainfall': float(latest_data.get('Rainfall', 0)),
                    'wind_speed': float(latest_data.get('Wind_Speed', 0)),
                    'pressure': float(latest_data.get('Pressure', 1013))
                })
        
        return cities_data
    
    def _get_monthly_trends(self) -> Dict:
        """Get monthly weather trends"""
        trends = {}
        
        if 'Month' in self.weather_data.columns:
            monthly_avg = self.weather_data.groupby('Month').agg({
                'Temperature': 'mean',
                'Humidity': 'mean', 
                'Rainfall': 'sum'
            }).round(2)
            
            trends = {
                'temperature': monthly_avg['Temperature'].to_dict(),
                'humidity': monthly_avg['Humidity'].to_dict(),
                'rainfall': monthly_avg['Rainfall'].to_dict()
            }
        
        return trends
    
    def _get_current_conditions(self) -> Dict:
        """Get current weather conditions summary"""
        if self.weather_data.empty:
            return {}
        
        latest_date = self.weather_data['Date'].max() if 'Date' in self.weather_data.columns else None
        
        current_data = self.weather_data.tail(20)  # Get recent data
        
        return {
            'avg_temperature': round(current_data['Temperature'].mean(), 1) if 'Temperature' in current_data else 0,
            'avg_humidity': round(current_data['Humidity'].mean(), 1) if 'Humidity' in current_data else 0,
            'total_rainfall': round(current_data['Rainfall'].sum(), 2) if 'Rainfall' in current_data else 0,
            'date': latest_date.isoformat() if latest_date else datetime.now().isoformat()
        }
    
    def _get_regional_summary(self) -> Dict:
        """Get weather summary by region/state"""
        regional_data = {}
        
        if 'State' in self.weather_data.columns:
            state_groups = self.weather_data.groupby('State')
            
            for state, group in state_groups:
                regional_data[state] = {
                    'avg_temperature': round(group['Temperature'].mean(), 1) if 'Temperature' in group else 0,
                    'avg_humidity': round(group['Humidity'].mean(), 1) if 'Humidity' in group else 0,
                    'total_rainfall': round(group['Rainfall'].sum(), 2) if 'Rainfall' in group else 0,
                    'cities_count': len(group['City'].unique()) if 'City' in group else 0
                }
        
        return regional_data
    
    def get_weather_data(self) -> Dict[str, Any]:
        """Get all processed weather data"""
        return self.processed_data
    
    def get_city_weather(self, city_name: str) -> Dict[str, Any]:
        """Get weather data for a specific city"""
        if self.weather_data is None:
            return {}
        
        city_data = self.weather_data[self.weather_data['City'].str.lower() == city_name.lower()]
        
        if city_data.empty:
            return {}
        
        latest = city_data.iloc[-1]
        
        return {
            'city': city_name,
            'state': latest.get('State', 'Unknown'),
            'current': {
                'temperature': float(latest.get('Temperature', 0)),
                'humidity': float(latest.get('Humidity', 0)),
                'rainfall': float(latest.get('Rainfall', 0)),
                'wind_speed': float(latest.get('Wind_Speed', 0)),
                'pressure': float(latest.get('Pressure', 1013))
            },
            'historical': {
                'avg_temperature': round(city_data['Temperature'].mean(), 1) if 'Temperature' in city_data else 0,
                'max_temperature': round(city_data['Temperature'].max(), 1) if 'Temperature' in city_data else 0,
                'min_temperature': round(city_data['Temperature'].min(), 1) if 'Temperature' in city_data else 0,
                'total_rainfall': round(city_data['Rainfall'].sum(), 2) if 'Rainfall' in city_data else 0
            }
        }
    
    def initialize(self) -> bool:
        """Initialize the service by downloading and processing data"""
        logger.info("Initializing Indian Weather Service...")
        
        # Download dataset (or use mock data if fails)
        download_success = self.download_dataset()
        
        # Load and process data
        process_success = self.load_and_process_data()
        
        logger.info(f"Service initialized. Download: {download_success}, Process: {process_success}")
        return process_success

# Create a global instance
indian_weather_service = IndianWeatherService()