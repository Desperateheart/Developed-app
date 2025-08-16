from pydantic import BaseModel
from typing import Optional, List, Dict
from datetime import datetime

# Disease Detection Schemas
class DiseaseDetectionResponse(BaseModel):
    disease_detected: bool
    disease_name: str
    confidence: float
    treatment: Optional[Dict]
    severity_analysis: Optional[Dict]
    affected_area: Optional[Dict]

# Farming Advice Schemas
class PlantingAdviceRequest(BaseModel):
    crop_type: str
    location: str
    soil_type: str
    season: str

class IrrigationAdviceRequest(BaseModel):
    crop_type: str
    soil_moisture: float
    weather_data: Dict
    growth_stage: str

class SoilAdviceRequest(BaseModel):
    soil_test_results: Dict
    crop_type: str
    previous_crops: List[str]

class FertilizerRequest(BaseModel):
    crop_type: str
    soil_data: Dict
    growth_stage: str

# Marketplace Schemas
class PriceSuggestionRequest(BaseModel):
    crop_type: str
    quantity: float
    quality_metrics: Dict
    location: str

class MarketListingRequest(BaseModel):
    seller_id: int
    crop_type: str
    quantity: float
    price: float
    location: str
    harvest_date: str
    description: str

# User Schemas
class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    farm_location: Optional[str]
    farm_size: Optional[float]

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None