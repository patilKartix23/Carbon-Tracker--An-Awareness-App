"""
Application configuration using Pydantic Settings (v2)
"""
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings"""

    # Pydantic v2 settings config
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="ignore",  # ignore any unrelated env vars like FLASK_DEBUG, DATABASE_URL, etc.
    )

    # App Configuration
    APP_NAME: str = "Climate Tracker API"
    VERSION: str = "2.0.0"
    DEBUG: bool = True
    ENVIRONMENT: str = "development"
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # Security
    SECRET_KEY: str = "dev-secret-key-change-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    ALGORITHM: str = "HS256"

    # CORS
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:3001",
        "http://localhost:3002",
        "http://localhost:3003",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001",
        "http://127.0.0.1:3002",
        "http://127.0.0.1:3003",
        "http://127.0.0.1:5173",
    ]
    ALLOWED_HOSTS: List[str] = ["*"]

    # Database Configuration
    # For smooth local dev, default to SQLite by leaving POSTGRES_HOST empty
    POSTGRES_HOST: str = ""
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = "climate_tracker"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "password"

    @property
    def postgres_url(self) -> str:
        # Use SQLite for development if PostgreSQL is not configured
        if self.ENVIRONMENT == "development" and not self.POSTGRES_HOST:
            return "sqlite:///./climate_tracker.db"
        return (
            f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    # MongoDB (Document Storage)
    MONGODB_URL: str = "mongodb://localhost:27017"
    MONGODB_DB: str = "climate_tracker_docs"

    # Redis (Caching & Background Tasks)
    REDIS_URL: str = "redis://localhost:6379/0"

    # External API Keys
    NASA_API_KEY: str = ""
    OPENWEATHER_API_KEY: str = ""
    NOAA_API_KEY: str = ""
    AIRVISUAL_API_KEY: str = ""

    # File Storage
    CLOUDINARY_CLOUD_NAME: str = ""
    CLOUDINARY_API_KEY: str = ""
    CLOUDINARY_API_SECRET: str = ""

    # AWS S3 (Alternative)
    AWS_ACCESS_KEY_ID: str = ""
    AWS_SECRET_ACCESS_KEY: str = ""
    AWS_BUCKET_NAME: str = ""
    AWS_REGION: str = "us-east-1"

    # ML Model Configuration
    MODEL_PATH: str = "models/"
    ENABLE_ML_FEATURES: bool = True

    # Logging
    LOG_LEVEL: str = "INFO"


# Create global settings instance
settings = Settings()
