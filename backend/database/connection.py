"""
Database connection management for PostgreSQL and Firebase
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import structlog
from core.config import settings

# Firebase client is optional in development
try:
    import firebase_admin
    from firebase_admin import credentials, firestore
    firebase_available = True
except ImportError:
    firebase_available = False

logger = structlog.get_logger()

# PostgreSQL Setup - wrapped in try-except for dev mode
try:
    engine = create_engine(
        settings.postgres_url,
        pool_pre_ping=True,
        pool_recycle=300,
        echo=settings.DEBUG
    )
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base = declarative_base()
    logger.info("Database engine created successfully")
except Exception as e:
    # Create a dummy engine for dev mode without database
    logger.warning(f"Could not create database engine, using fallback: {e}")
    from sqlalchemy import create_engine as ce
    engine = ce("sqlite:///:memory:", echo=False)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base = declarative_base()

# Firebase Setup (optional)
firebase_db = None

async def init_db():
    """Initialize database connections"""
    global firebase_db
    
    try:
        # Create PostgreSQL/SQLite tables
        Base.metadata.create_all(bind=engine)
        logger.info("Connected to database", database=settings.postgres_url)
        
        # Try to initialize Firebase (optional for development)
        if firebase_available and settings.FIREBASE_CREDENTIALS_PATH:
            try:
                if not firebase_admin._apps:
                    cred = credentials.Certificate(settings.FIREBASE_CREDENTIALS_PATH)
                    firebase_admin.initialize_app(cred)
                firebase_db = firestore.client()
                logger.info("Connected to Firebase Firestore")
            except Exception as firebase_error:
                logger.warning("Firebase not available, using SQLite storage", error=str(firebase_error))
        else:
            logger.warning("Firebase not configured; using SQLite only")
        
    except Exception as e:
        logger.warning("Database not available - running without database features", error=str(e))
        # Don't raise - allow app to start without database for CCUS and other features

async def close_db():
    """Close database connections"""
    global firebase_db
    
    if firebase_db:
        # Firebase connections are managed automatically
        logger.info("Firebase connection closed")

def get_db():
    """Get PostgreSQL database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_firestore():
    """Get Firebase Firestore database instance"""
    return firebase_db
