"""
Database connection management for PostgreSQL and MongoDB
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
# MongoDB client is optional in development. Import defensively.
try:
    from motor.motor_asyncio import AsyncIOMotorClient  # type: ignore
except Exception:  # ModuleNotFoundError or others
    AsyncIOMotorClient = None  # type: ignore
import structlog
from core.config import settings

logger = structlog.get_logger()

# PostgreSQL Setup
engine = create_engine(
    settings.postgres_url,
    pool_pre_ping=True,
    pool_recycle=300,
    echo=settings.DEBUG
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# MongoDB Setup (optional)
mongodb_client = None
mongodb_db = None

async def init_db():
    """Initialize database connections"""
    global mongodb_client, mongodb_db
    
    try:
        # Create PostgreSQL/SQLite tables
        Base.metadata.create_all(bind=engine)
        logger.info("Connected to database", database=settings.postgres_url)
        
        # Try to initialize MongoDB (optional for development)
        if AsyncIOMotorClient is not None:
            try:
                mongodb_client_local = AsyncIOMotorClient(settings.MONGODB_URL)
                # Test MongoDB connection
                await mongodb_client_local.admin.command('ping')
                logger.info("Connected to MongoDB", database=settings.MONGODB_DB)
                # Assign only after successful ping
                global mongodb_client, mongodb_db
                mongodb_client = mongodb_client_local
                mongodb_db = mongodb_client_local[settings.MONGODB_DB]
            except Exception as mongo_error:
                logger.warning("MongoDB not available, using mock storage", error=str(mongo_error))
        else:
            logger.warning("motor not installed; skipping MongoDB initialization")
        
    except Exception as e:
        logger.error("Failed to initialize databases", error=str(e))
        raise

async def close_db():
    """Close database connections"""
    global mongodb_client
    
    if mongodb_client:
        mongodb_client.close()
        logger.info("Closed MongoDB connection")

def get_db():
    """Get PostgreSQL database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_mongodb():
    """Get MongoDB database instance"""
    return mongodb_db
