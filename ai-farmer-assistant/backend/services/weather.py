from typing import Dict, List, Optional
from datetime import datetime, timedelta
import random
import json

class WeatherService:
    """
    Service for weather data and farming-specific weather alerts
    """
    
    def __init__(self):
        # In production, this would connect to real weather APIs
        self.weather_conditions = [
            "Clear", "Partly Cloudy", "Cloudy", "Light Rain", 
            "Moderate Rain", "Heavy Rain", "Thunderstorm", "Foggy"
        ]
        
    async def get_current_weather(self, location: str) -> Dict:
        """
        Get current weather for a location
        """
        # Mock weather data - in production, use real weather API
        temperature = random.randint(15, 35)
        humidity = random.randint(40, 90)
        wind_speed = random.randint(5, 25)
        
        weather = {
            "location": location,
            "timestamp": datetime.now().isoformat(),
            "current": {
                "temperature": {
                    "value": temperature,
                    "unit": "°C",
                    "feels_like": temperature + random.randint(-3, 3)
                },
                "humidity": f"{humidity}%",
                "wind": {
                    "speed": f"{wind_speed} km/h",
                    "direction": random.choice(["N", "NE", "E", "SE", "S", "SW", "W", "NW"])
                },
                "pressure": f"{random.randint(1000, 1020)} hPa",
                "visibility": f"{random.randint(5, 10)} km",
                "condition": random.choice(self.weather_conditions),
                "uv_index": random.randint(1, 11),
                "precipitation": f"{random.randint(0, 10)} mm"
            },
            "sun": {
                "sunrise": "06:15",
                "sunset": "18:45"
            },
            "farming_impact": {
                "irrigation_needed": humidity < 60,
                "spray_conditions": wind_speed < 15 and humidity < 80,
                "harvest_suitable": humidity < 70 and "Rain" not in random.choice(self.weather_conditions),
                "planting_suitable": temperature > 15 and temperature < 30
            }
        }
        
        return weather
    
    async def get_forecast(self, location: str, days: int = 7) -> Dict:
        """
        Get weather forecast for a location
        """
        forecast_data = []
        base_temp = random.randint(18, 28)
        
        for i in range(days):
            date = datetime.now() + timedelta(days=i)
            temp_variation = random.randint(-5, 5)
            
            forecast_data.append({
                "date": date.strftime("%Y-%m-%d"),
                "day_name": date.strftime("%A"),
                "temperature": {
                    "min": base_temp + temp_variation - 5,
                    "max": base_temp + temp_variation + 8,
                    "average": base_temp + temp_variation
                },
                "humidity": {
                    "min": random.randint(30, 50),
                    "max": random.randint(60, 90),
                    "average": random.randint(45, 75)
                },
                "precipitation": {
                    "probability": random.randint(0, 100),
                    "amount": f"{random.randint(0, 20)} mm"
                },
                "wind": {
                    "speed": f"{random.randint(5, 25)} km/h",
                    "direction": random.choice(["N", "NE", "E", "SE", "S", "SW", "W", "NW"])
                },
                "condition": random.choice(self.weather_conditions),
                "uv_index": random.randint(3, 10),
                "farming_activities": self._get_daily_farming_activities(i)
            })
        
        # Calculate summary statistics
        avg_temp = sum(d["temperature"]["average"] for d in forecast_data) / len(forecast_data)
        total_precipitation = sum(int(d["precipitation"]["amount"].split()[0]) for d in forecast_data)
        rainy_days = sum(1 for d in forecast_data if d["precipitation"]["probability"] > 50)
        
        return {
            "location": location,
            "forecast_period": f"{days} days",
            "generated_at": datetime.now().isoformat(),
            "daily_forecast": forecast_data,
            "summary": {
                "average_temperature": round(avg_temp, 1),
                "total_precipitation": f"{total_precipitation} mm",
                "rainy_days": rainy_days,
                "dry_days": days - rainy_days,
                "trend": self._determine_weather_trend(forecast_data)
            },
            "farming_recommendations": self._get_weekly_farming_recommendations(forecast_data),
            "alerts": self._generate_weather_alerts(forecast_data)
        }
    
    async def get_farming_alerts(self, location: str) -> Dict:
        """
        Get weather alerts specific to farming activities
        """
        # Generate mock alerts based on conditions
        alerts = []
        
        # Temperature alerts
        current_temp = random.randint(10, 40)
        if current_temp < 15:
            alerts.append({
                "type": "FROST_WARNING",
                "severity": "HIGH",
                "message": "Frost expected tonight. Protect sensitive crops.",
                "affected_crops": ["tomato", "pepper", "cucumber"],
                "recommended_actions": [
                    "Cover plants with frost cloth",
                    "Water soil before sunset",
                    "Harvest ripe produce immediately"
                ],
                "valid_until": (datetime.now() + timedelta(hours=12)).isoformat()
            })
        elif current_temp > 35:
            alerts.append({
                "type": "HEAT_STRESS",
                "severity": "MODERATE",
                "message": "High temperatures expected. Increase irrigation.",
                "affected_crops": ["all"],
                "recommended_actions": [
                    "Increase watering frequency",
                    "Apply mulch to retain moisture",
                    "Provide shade for sensitive plants",
                    "Water early morning or late evening"
                ],
                "valid_until": (datetime.now() + timedelta(days=2)).isoformat()
            })
        
        # Precipitation alerts
        if random.random() > 0.6:
            alerts.append({
                "type": "HEAVY_RAIN",
                "severity": "MODERATE",
                "message": "Heavy rain expected in next 24 hours.",
                "affected_crops": ["all"],
                "recommended_actions": [
                    "Ensure proper drainage",
                    "Postpone fertilizer application",
                    "Harvest mature crops",
                    "Check for disease after rain"
                ],
                "valid_until": (datetime.now() + timedelta(days=1)).isoformat()
            })
        
        # Wind alerts
        if random.random() > 0.7:
            alerts.append({
                "type": "STRONG_WIND",
                "severity": "LOW",
                "message": "Strong winds expected. Secure tall plants.",
                "affected_crops": ["corn", "tomato"],
                "recommended_actions": [
                    "Stake tall plants",
                    "Postpone spraying activities",
                    "Check greenhouse structures"
                ],
                "valid_until": (datetime.now() + timedelta(hours=6)).isoformat()
            })
        
        # Disease risk alerts
        if random.random() > 0.5:
            alerts.append({
                "type": "DISEASE_RISK",
                "severity": "MODERATE",
                "message": "High humidity creates disease risk.",
                "affected_crops": ["tomato", "potato", "grape"],
                "recommended_actions": [
                    "Apply preventive fungicide",
                    "Improve air circulation",
                    "Remove affected leaves",
                    "Monitor plants closely"
                ],
                "valid_until": (datetime.now() + timedelta(days=3)).isoformat()
            })
        
        return {
            "location": location,
            "generated_at": datetime.now().isoformat(),
            "active_alerts": len(alerts),
            "alerts": alerts,
            "general_conditions": {
                "irrigation_index": random.choice(["High", "Moderate", "Low"]),
                "disease_risk": random.choice(["High", "Moderate", "Low"]),
                "pest_activity": random.choice(["High", "Moderate", "Low"]),
                "optimal_for_planting": random.choice([True, False]),
                "optimal_for_harvesting": random.choice([True, False])
            },
            "next_update": (datetime.now() + timedelta(hours=6)).isoformat()
        }
    
    # Helper methods
    def _get_daily_farming_activities(self, day_offset: int) -> Dict:
        """Get recommended farming activities for a specific day"""
        activities = {
            "suitable_for": [],
            "avoid": []
        }
        
        # Random recommendations based on weather
        if random.random() > 0.5:
            activities["suitable_for"].extend(["planting", "transplanting"])
        else:
            activities["avoid"].append("planting")
        
        if random.random() > 0.4:
            activities["suitable_for"].append("fertilizing")
        
        if random.random() > 0.3:
            activities["suitable_for"].append("harvesting")
        else:
            activities["avoid"].append("harvesting")
        
        if random.random() > 0.6:
            activities["suitable_for"].append("spraying")
        else:
            activities["avoid"].append("spraying")
        
        return activities
    
    def _determine_weather_trend(self, forecast_data: List[Dict]) -> str:
        """Determine overall weather trend"""
        temps = [d["temperature"]["average"] for d in forecast_data]
        precipitation = [d["precipitation"]["probability"] for d in forecast_data]
        
        temp_trend = "stable"
        if temps[-1] > temps[0] + 3:
            temp_trend = "warming"
        elif temps[-1] < temps[0] - 3:
            temp_trend = "cooling"
        
        rain_trend = "dry"
        if sum(precipitation) / len(precipitation) > 50:
            rain_trend = "wet"
        elif sum(precipitation) / len(precipitation) > 30:
            rain_trend = "mixed"
        
        return f"{temp_trend} and {rain_trend}"
    
    def _get_weekly_farming_recommendations(self, forecast_data: List[Dict]) -> List[str]:
        """Get farming recommendations based on weekly forecast"""
        recommendations = []
        
        # Analyze forecast
        avg_temp = sum(d["temperature"]["average"] for d in forecast_data) / len(forecast_data)
        total_rain_prob = sum(d["precipitation"]["probability"] for d in forecast_data) / len(forecast_data)
        
        if avg_temp > 30:
            recommendations.append("Increase irrigation frequency due to high temperatures")
        elif avg_temp < 15:
            recommendations.append("Protect sensitive crops from cold temperatures")
        
        if total_rain_prob > 60:
            recommendations.append("Prepare drainage systems for expected rainfall")
            recommendations.append("Apply fungicides preventively before rain")
        elif total_rain_prob < 20:
            recommendations.append("Plan irrigation schedule for dry period ahead")
        
        # General recommendations
        recommendations.extend([
            "Monitor soil moisture levels regularly",
            "Check weather updates before spraying",
            "Plan harvesting for dry days"
        ])
        
        return recommendations
    
    def _generate_weather_alerts(self, forecast_data: List[Dict]) -> List[Dict]:
        """Generate weather alerts from forecast data"""
        alerts = []
        
        for i, day in enumerate(forecast_data[:3]):  # Check next 3 days
            # Check for extreme temperatures
            if day["temperature"]["max"] > 35:
                alerts.append({
                    "day": day["date"],
                    "type": "heat",
                    "message": f"High temperature ({day['temperature']['max']}°C) expected"
                })
            elif day["temperature"]["min"] < 10:
                alerts.append({
                    "day": day["date"],
                    "type": "cold",
                    "message": f"Low temperature ({day['temperature']['min']}°C) expected"
                })
            
            # Check for high precipitation
            if day["precipitation"]["probability"] > 80:
                alerts.append({
                    "day": day["date"],
                    "type": "rain",
                    "message": f"High chance of rain ({day['precipitation']['probability']}%)"
                })
        
        return alerts