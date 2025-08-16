from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./farmer_assistant.db")

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Database Models
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    farm_location = Column(String, nullable=True)
    farm_size = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)

class DiseaseDetection(Base):
    __tablename__ = "disease_detections"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=True)
    crop_type = Column(String)
    disease_name = Column(String)
    confidence = Column(Float)
    severity = Column(String)
    image_path = Column(String, nullable=True)
    treatment_applied = Column(Text, nullable=True)
    detection_date = Column(DateTime, default=datetime.utcnow)

class MarketListing(Base):
    __tablename__ = "market_listings"
    
    id = Column(Integer, primary_key=True, index=True)
    seller_id = Column(Integer)
    crop_type = Column(String)
    quantity = Column(Float)
    price_per_kg = Column(Float)
    location = Column(String)
    harvest_date = Column(DateTime)
    listing_date = Column(DateTime, default=datetime.utcnow)
    expiry_date = Column(DateTime)
    status = Column(String, default="active")
    description = Column(Text)
    views = Column(Integer, default=0)
    inquiries = Column(Integer, default=0)

class FarmingAdviceLog(Base):
    __tablename__ = "farming_advice_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=True)
    advice_type = Column(String)  # planting, irrigation, soil, fertilizer
    crop_type = Column(String)
    location = Column(String, nullable=True)
    request_data = Column(Text)  # JSON string
    response_data = Column(Text)  # JSON string
    created_at = Column(DateTime, default=datetime.utcnow)

class WeatherAlert(Base):
    __tablename__ = "weather_alerts"
    
    id = Column(Integer, primary_key=True, index=True)
    location = Column(String)
    alert_type = Column(String)
    severity = Column(String)
    message = Column(Text)
    affected_crops = Column(Text)  # JSON string
    valid_until = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)

# Database initialization
async def init_db():
    """Initialize database tables"""
    Base.metadata.create_all(bind=engine)

async def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()