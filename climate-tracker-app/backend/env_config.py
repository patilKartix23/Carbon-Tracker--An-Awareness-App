"""
Environment configuration for OpenWeatherMap API
"""
import os

# Set the OpenWeatherMap API key
os.environ['OPENWEATHER_API_KEY'] = '7404ac03aa86e4f9b52cdabb108c6dc8'

# Bengaluru coordinates
os.environ['DEFAULT_LAT'] = '12.9716'
os.environ['DEFAULT_LON'] = '77.5946'
os.environ['DEFAULT_CITY'] = 'Bengaluru'

print("✅ OpenWeatherMap API configured for Bengaluru weather data")
