from fastapi import FastAPI, File, UploadFile, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import List, Optional
import uvicorn
from datetime import datetime
import os
from dotenv import load_dotenv

# Import our modules
from backend.models.database import init_db, get_db
from backend.services.disease_detection import DiseaseDetectionService
from backend.services.farming_advice import FarmingAdviceService
from backend.services.marketplace import MarketplaceService
from backend.services.weather import WeatherService
from backend.schemas import *
from backend.auth import get_current_user, create_access_token, verify_password, get_password_hash

load_dotenv()

app = FastAPI(
    title="AI Farmer Assistant",
    description="AI-powered farming assistant for disease detection, advice, and marketplace",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
disease_service = DiseaseDetectionService()
farming_service = FarmingAdviceService()
marketplace_service = MarketplaceService()
weather_service = WeatherService()

@app.on_event("startup")
async def startup():
    """Initialize database and load AI models on startup"""
    await init_db()
    await disease_service.load_model()
    print("AI Farmer Assistant API is ready!")

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to AI Farmer Assistant API",
        "version": "1.0.0",
        "endpoints": {
            "disease_detection": "/api/disease/detect",
            "farming_advice": "/api/advice",
            "marketplace": "/api/marketplace",
            "weather": "/api/weather"
        }
    }

# Disease Detection Endpoints
@app.post("/api/disease/detect")
async def detect_disease(
    file: UploadFile = File(...),
    crop_type: Optional[str] = None
):
    """
    Detect crop diseases from uploaded image
    """
    try:
        # Validate file type
        if not file.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        # Read image data
        image_data = await file.read()
        
        # Perform disease detection
        result = await disease_service.detect_disease(image_data, crop_type)
        
        return {
            "success": True,
            "data": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/disease/history")
async def get_disease_history(
    user_id: Optional[int] = None,
    limit: int = 10
):
    """Get disease detection history"""
    try:
        history = await disease_service.get_history(user_id, limit)
        return {
            "success": True,
            "data": history
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Farming Advice Endpoints
@app.post("/api/advice/planting")
async def get_planting_advice(request: PlantingAdviceRequest):
    """
    Get personalized planting advice based on location, crop, and conditions
    """
    try:
        advice = await farming_service.get_planting_advice(
            crop_type=request.crop_type,
            location=request.location,
            soil_type=request.soil_type,
            season=request.season
        )
        return {
            "success": True,
            "data": advice
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/advice/irrigation")
async def get_irrigation_advice(request: IrrigationAdviceRequest):
    """
    Get irrigation recommendations based on crop and weather
    """
    try:
        advice = await farming_service.get_irrigation_advice(
            crop_type=request.crop_type,
            soil_moisture=request.soil_moisture,
            weather_data=request.weather_data,
            growth_stage=request.growth_stage
        )
        return {
            "success": True,
            "data": advice
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/advice/soil")
async def get_soil_advice(request: SoilAdviceRequest):
    """
    Get soil management recommendations
    """
    try:
        advice = await farming_service.get_soil_advice(
            soil_test_results=request.soil_test_results,
            crop_type=request.crop_type,
            previous_crops=request.previous_crops
        )
        return {
            "success": True,
            "data": advice
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/advice/fertilizer")
async def get_fertilizer_recommendations(request: FertilizerRequest):
    """
    Get fertilizer recommendations based on soil and crop
    """
    try:
        recommendations = await farming_service.get_fertilizer_recommendations(
            crop_type=request.crop_type,
            soil_data=request.soil_data,
            growth_stage=request.growth_stage
        )
        return {
            "success": True,
            "data": recommendations
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Marketplace Endpoints
@app.get("/api/marketplace/prices")
async def get_market_prices(
    crop_type: str,
    location: Optional[str] = None,
    quality_grade: Optional[str] = None
):
    """
    Get current market prices for crops
    """
    try:
        prices = await marketplace_service.get_market_prices(
            crop_type=crop_type,
            location=location,
            quality_grade=quality_grade
        )
        return {
            "success": True,
            "data": prices
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/marketplace/price-suggestion")
async def suggest_fair_price(request: PriceSuggestionRequest):
    """
    Suggest fair price based on quality, quantity, and market conditions
    """
    try:
        suggestion = await marketplace_service.suggest_fair_price(
            crop_type=request.crop_type,
            quantity=request.quantity,
            quality_metrics=request.quality_metrics,
            location=request.location
        )
        return {
            "success": True,
            "data": suggestion
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/marketplace/buyers")
async def find_buyers(
    crop_type: str,
    location: str,
    quantity: float,
    delivery_date: Optional[str] = None
):
    """
    Find potential buyers for crops
    """
    try:
        buyers = await marketplace_service.find_buyers(
            crop_type=crop_type,
            location=location,
            quantity=quantity,
            delivery_date=delivery_date
        )
        return {
            "success": True,
            "data": buyers
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/marketplace/listing")
async def create_listing(request: MarketListingRequest):
    """
    Create a new marketplace listing
    """
    try:
        listing = await marketplace_service.create_listing(
            seller_id=request.seller_id,
            crop_type=request.crop_type,
            quantity=request.quantity,
            price=request.price,
            location=request.location,
            harvest_date=request.harvest_date,
            description=request.description
        )
        return {
            "success": True,
            "data": listing
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/marketplace/listings")
async def get_listings(
    crop_type: Optional[str] = None,
    location: Optional[str] = None,
    min_quantity: Optional[float] = None,
    max_price: Optional[float] = None
):
    """
    Get marketplace listings with filters
    """
    try:
        listings = await marketplace_service.get_listings(
            crop_type=crop_type,
            location=location,
            min_quantity=min_quantity,
            max_price=max_price
        )
        return {
            "success": True,
            "data": listings
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Weather Endpoints
@app.get("/api/weather/current")
async def get_current_weather(location: str):
    """
    Get current weather for a location
    """
    try:
        weather = await weather_service.get_current_weather(location)
        return {
            "success": True,
            "data": weather
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/weather/forecast")
async def get_weather_forecast(location: str, days: int = 7):
    """
    Get weather forecast for a location
    """
    try:
        forecast = await weather_service.get_forecast(location, days)
        return {
            "success": True,
            "data": forecast
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/weather/alerts")
async def get_weather_alerts(location: str):
    """
    Get weather alerts for farming
    """
    try:
        alerts = await weather_service.get_farming_alerts(location)
        return {
            "success": True,
            "data": alerts
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Analytics Endpoints
@app.get("/api/analytics/crop-performance")
async def get_crop_performance(
    user_id: int,
    season: Optional[str] = None
):
    """
    Get crop performance analytics
    """
    try:
        analytics = await farming_service.get_crop_performance(user_id, season)
        return {
            "success": True,
            "data": analytics
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/analytics/market-trends")
async def get_market_trends(
    crop_type: str,
    period: str = "monthly"
):
    """
    Get market trend analytics
    """
    try:
        trends = await marketplace_service.get_market_trends(crop_type, period)
        return {
            "success": True,
            "data": trends
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )