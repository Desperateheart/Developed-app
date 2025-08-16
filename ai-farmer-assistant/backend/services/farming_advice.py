from typing import Dict, List, Optional
from datetime import datetime, timedelta
import json
import random

class FarmingAdviceService:
    """
    Service for providing farming advice including planting, irrigation, and soil management
    """
    
    def __init__(self):
        self.crop_data = {
            "tomato": {
                "planting": {
                    "optimal_temp": "18-27°C",
                    "soil_ph": "6.0-6.8",
                    "spacing": "45-60cm",
                    "depth": "0.6-1.25cm",
                    "germination": "5-10 days",
                    "harvest_time": "60-80 days",
                    "seasons": ["spring", "summer"],
                    "water_needs": "moderate to high",
                    "sunlight": "full sun (6-8 hours)"
                },
                "irrigation": {
                    "seedling": "light daily watering",
                    "vegetative": "2-3 times per week",
                    "flowering": "deep watering 2 times per week",
                    "fruiting": "consistent moisture, avoid overwatering",
                    "water_amount": "1-2 inches per week"
                },
                "fertilizer": {
                    "npk_ratio": "5-10-10",
                    "organic_options": ["compost", "aged manure", "bone meal"],
                    "application_schedule": "Every 2-3 weeks during growing season"
                }
            },
            "wheat": {
                "planting": {
                    "optimal_temp": "12-25°C",
                    "soil_ph": "6.0-7.0",
                    "spacing": "15-22cm between rows",
                    "depth": "2.5-5cm",
                    "germination": "7-14 days",
                    "harvest_time": "100-130 days",
                    "seasons": ["fall", "spring"],
                    "water_needs": "moderate",
                    "sunlight": "full sun"
                },
                "irrigation": {
                    "seedling": "keep soil moist",
                    "tillering": "moderate watering",
                    "stem_elongation": "increased water needs",
                    "grain_filling": "critical water period",
                    "water_amount": "12-16 inches total"
                },
                "fertilizer": {
                    "npk_ratio": "15-15-15",
                    "organic_options": ["compost", "green manure"],
                    "application_schedule": "At planting and mid-season"
                }
            },
            "rice": {
                "planting": {
                    "optimal_temp": "20-35°C",
                    "soil_ph": "5.5-7.0",
                    "spacing": "15-20cm",
                    "depth": "1-2cm",
                    "germination": "5-7 days",
                    "harvest_time": "90-120 days",
                    "seasons": ["summer", "monsoon"],
                    "water_needs": "high (flooded fields)",
                    "sunlight": "full sun"
                },
                "irrigation": {
                    "seedling": "maintain 2-5cm water",
                    "tillering": "5-7cm water depth",
                    "panicle": "maintain flooding",
                    "grain_filling": "reduce to 2-3cm",
                    "water_amount": "1200-1500mm total"
                },
                "fertilizer": {
                    "npk_ratio": "20-10-10",
                    "organic_options": ["green manure", "azolla"],
                    "application_schedule": "Basal, tillering, and panicle stages"
                }
            },
            "corn": {
                "planting": {
                    "optimal_temp": "18-32°C",
                    "soil_ph": "5.8-7.0",
                    "spacing": "20-30cm",
                    "depth": "2.5-5cm",
                    "germination": "7-10 days",
                    "harvest_time": "60-100 days",
                    "seasons": ["spring", "summer"],
                    "water_needs": "high",
                    "sunlight": "full sun"
                },
                "irrigation": {
                    "seedling": "light frequent watering",
                    "vegetative": "1 inch per week",
                    "tasseling": "critical water period",
                    "grain_filling": "maintain moisture",
                    "water_amount": "20-30 inches total"
                },
                "fertilizer": {
                    "npk_ratio": "10-10-10",
                    "organic_options": ["compost", "fish emulsion"],
                    "application_schedule": "At planting and knee-high stage"
                }
            },
            "potato": {
                "planting": {
                    "optimal_temp": "15-20°C",
                    "soil_ph": "5.0-6.5",
                    "spacing": "30-40cm",
                    "depth": "10-15cm",
                    "germination": "14-21 days",
                    "harvest_time": "70-120 days",
                    "seasons": ["spring", "fall"],
                    "water_needs": "moderate to high",
                    "sunlight": "full sun"
                },
                "irrigation": {
                    "sprouting": "keep soil moist",
                    "vegetative": "1-2 inches per week",
                    "tuber_formation": "consistent moisture critical",
                    "maturation": "reduce watering",
                    "water_amount": "1-2 inches per week"
                },
                "fertilizer": {
                    "npk_ratio": "10-10-10",
                    "organic_options": ["compost", "aged manure"],
                    "application_schedule": "At planting and hilling"
                }
            }
        }
        
        self.soil_types = {
            "clay": {
                "characteristics": "Heavy, holds water, slow drainage",
                "improvements": ["Add organic matter", "Use raised beds", "Add sand or perlite"],
                "best_crops": ["rice", "broccoli", "cabbage"],
                "challenges": ["Poor drainage", "Compaction", "Slow warming"]
            },
            "sandy": {
                "characteristics": "Light, fast drainage, low nutrients",
                "improvements": ["Add compost", "Use mulch", "Frequent fertilization"],
                "best_crops": ["carrots", "potatoes", "lettuce"],
                "challenges": ["Water retention", "Nutrient leaching"]
            },
            "loam": {
                "characteristics": "Ideal mix, good drainage and retention",
                "improvements": ["Maintain organic matter", "Regular testing"],
                "best_crops": ["most vegetables", "fruits", "grains"],
                "challenges": ["Few challenges when maintained"]
            },
            "silt": {
                "characteristics": "Smooth, retains moisture, fertile",
                "improvements": ["Add organic matter", "Avoid compaction"],
                "best_crops": ["vegetables", "fruits", "grains"],
                "challenges": ["Compaction", "Erosion"]
            }
        }
    
    async def get_planting_advice(self, crop_type: str, location: str, 
                                  soil_type: str, season: str) -> Dict:
        """
        Get personalized planting advice
        """
        crop_type = crop_type.lower()
        soil_type = soil_type.lower()
        
        # Get crop-specific data
        crop_info = self.crop_data.get(crop_type, self.crop_data["tomato"])
        soil_info = self.soil_types.get(soil_type, self.soil_types["loam"])
        
        # Generate planting calendar
        planting_calendar = self._generate_planting_calendar(crop_type, season)
        
        # Check seasonal compatibility
        season_compatible = season.lower() in crop_info["planting"].get("seasons", [])
        
        advice = {
            "crop": crop_type,
            "location": location,
            "soil_type": soil_type,
            "season": season,
            "compatibility": {
                "season_compatible": season_compatible,
                "soil_suitable": crop_type not in ["rice"] or soil_type == "clay"
            },
            "planting_guide": {
                "optimal_temperature": crop_info["planting"]["optimal_temp"],
                "soil_ph": crop_info["planting"]["soil_ph"],
                "planting_depth": crop_info["planting"]["depth"],
                "spacing": crop_info["planting"]["spacing"],
                "germination_time": crop_info["planting"]["germination"],
                "harvest_time": crop_info["planting"]["harvest_time"],
                "sunlight_needs": crop_info["planting"]["sunlight"]
            },
            "soil_preparation": {
                "current_soil": soil_info["characteristics"],
                "improvements_needed": soil_info["improvements"],
                "amendments": self._get_soil_amendments(soil_type, crop_type)
            },
            "planting_calendar": planting_calendar,
            "companion_plants": self._get_companion_plants(crop_type),
            "common_mistakes": self._get_common_mistakes(crop_type),
            "tips": self._generate_planting_tips(crop_type, soil_type, season)
        }
        
        return advice
    
    async def get_irrigation_advice(self, crop_type: str, soil_moisture: float,
                                   weather_data: Dict, growth_stage: str) -> Dict:
        """
        Get irrigation recommendations
        """
        crop_type = crop_type.lower()
        crop_info = self.crop_data.get(crop_type, self.crop_data["tomato"])
        
        # Determine irrigation needs based on multiple factors
        irrigation_need = self._calculate_irrigation_need(
            soil_moisture, weather_data, growth_stage, crop_type
        )
        
        # Get stage-specific advice
        stage_advice = crop_info["irrigation"].get(
            growth_stage, 
            "Maintain consistent moisture"
        )
        
        advice = {
            "crop": crop_type,
            "current_conditions": {
                "soil_moisture": f"{soil_moisture}%",
                "growth_stage": growth_stage,
                "weather": weather_data
            },
            "irrigation_recommendation": {
                "immediate_action": irrigation_need["action"],
                "water_amount": irrigation_need["amount"],
                "frequency": irrigation_need["frequency"],
                "method": irrigation_need["method"],
                "timing": irrigation_need["timing"]
            },
            "stage_specific_advice": stage_advice,
            "water_conservation_tips": [
                "Use drip irrigation for efficiency",
                "Apply mulch to retain moisture",
                "Water early morning or late evening",
                "Monitor soil moisture regularly",
                "Collect rainwater when possible"
            ],
            "signs_of_water_stress": {
                "underwatering": [
                    "Wilting leaves",
                    "Dry, crumbly soil",
                    "Slow growth",
                    "Leaf drop"
                ],
                "overwatering": [
                    "Yellow leaves",
                    "Root rot",
                    "Fungal growth",
                    "Waterlogged soil"
                ]
            },
            "irrigation_schedule": self._generate_irrigation_schedule(
                crop_type, growth_stage, weather_data
            )
        }
        
        return advice
    
    async def get_soil_advice(self, soil_test_results: Dict, 
                             crop_type: str, previous_crops: List[str]) -> Dict:
        """
        Get soil management recommendations
        """
        # Analyze soil test results
        soil_analysis = self._analyze_soil_test(soil_test_results)
        
        # Generate recommendations
        recommendations = {
            "soil_health_score": soil_analysis["health_score"],
            "current_status": soil_analysis["status"],
            "nutrient_analysis": {
                "nitrogen": soil_analysis["nutrients"]["N"],
                "phosphorus": soil_analysis["nutrients"]["P"],
                "potassium": soil_analysis["nutrients"]["K"],
                "ph_level": soil_test_results.get("ph", 6.5),
                "organic_matter": soil_test_results.get("organic_matter", "moderate")
            },
            "amendments_needed": soil_analysis["amendments"],
            "crop_rotation_advice": self._get_rotation_advice(
                crop_type, previous_crops
            ),
            "organic_improvements": [
                "Add compost (2-3 inches annually)",
                "Use cover crops in off-season",
                "Apply aged manure",
                "Mulch regularly",
                "Minimize tillage"
            ],
            "timeline": {
                "immediate": soil_analysis["immediate_actions"],
                "before_planting": soil_analysis["pre_planting"],
                "during_season": soil_analysis["maintenance"]
            },
            "testing_schedule": "Test soil every 2-3 years or when changing crops"
        }
        
        return recommendations
    
    async def get_fertilizer_recommendations(self, crop_type: str, 
                                           soil_data: Dict, growth_stage: str) -> Dict:
        """
        Get fertilizer recommendations
        """
        crop_type = crop_type.lower()
        crop_info = self.crop_data.get(crop_type, self.crop_data["tomato"])
        
        # Calculate fertilizer needs
        fertilizer_needs = self._calculate_fertilizer_needs(
            crop_type, soil_data, growth_stage
        )
        
        recommendations = {
            "crop": crop_type,
            "growth_stage": growth_stage,
            "recommended_fertilizer": {
                "npk_ratio": crop_info["fertilizer"]["npk_ratio"],
                "amount": fertilizer_needs["amount"],
                "frequency": crop_info["fertilizer"]["application_schedule"],
                "application_method": fertilizer_needs["method"]
            },
            "organic_alternatives": crop_info["fertilizer"]["organic_options"],
            "micronutrients": fertilizer_needs["micronutrients"],
            "application_tips": [
                "Water after application",
                "Avoid fertilizing during hot weather",
                "Don't over-fertilize - follow recommendations",
                "Keep fertilizer away from stems",
                "Consider soil testing before major applications"
            ],
            "stage_specific": fertilizer_needs["stage_specific"],
            "warning_signs": {
                "over_fertilization": [
                    "Excessive foliage growth",
                    "Reduced fruiting",
                    "Salt buildup",
                    "Leaf burn"
                ],
                "deficiency_signs": fertilizer_needs["deficiency_signs"]
            }
        }
        
        return recommendations
    
    async def get_crop_performance(self, user_id: int, season: Optional[str]) -> Dict:
        """
        Get crop performance analytics
        """
        # In production, this would fetch from database
        # Mock data for demonstration
        performance = {
            "user_id": user_id,
            "season": season or "current",
            "overall_yield": {
                "total_harvest": "450 kg",
                "compared_to_average": "+15%",
                "quality_grade": "A"
            },
            "crop_breakdown": [
                {
                    "crop": "tomato",
                    "area": "0.5 hectares",
                    "yield": "150 kg",
                    "revenue": "$450",
                    "roi": "180%"
                },
                {
                    "crop": "potato",
                    "area": "0.3 hectares",
                    "yield": "200 kg",
                    "revenue": "$300",
                    "roi": "150%"
                }
            ],
            "disease_impact": {
                "incidents": 3,
                "yield_loss": "5%",
                "treatment_cost": "$50"
            },
            "resource_usage": {
                "water": "15000 liters",
                "fertilizer": "50 kg",
                "pesticides": "5 liters"
            },
            "recommendations": [
                "Consider crop rotation for better soil health",
                "Increase organic matter content",
                "Optimize irrigation schedule"
            ]
        }
        
        return performance
    
    # Helper methods
    def _generate_planting_calendar(self, crop_type: str, season: str) -> List[Dict]:
        """Generate a planting calendar"""
        today = datetime.now()
        calendar = []
        
        tasks = [
            {"week": 0, "task": "Soil preparation and testing"},
            {"week": 1, "task": "Add amendments and fertilizer"},
            {"week": 2, "task": "Planting/Sowing"},
            {"week": 3, "task": "First watering and mulching"},
            {"week": 4, "task": "Thinning and weeding"},
            {"week": 6, "task": "First fertilizer application"},
            {"week": 8, "task": "Pest and disease monitoring"},
            {"week": 10, "task": "Second fertilizer application"},
            {"week": 12, "task": "Support/staking if needed"}
        ]
        
        for task in tasks:
            date = today + timedelta(weeks=task["week"])
            calendar.append({
                "date": date.strftime("%Y-%m-%d"),
                "week": task["week"],
                "task": task["task"]
            })
        
        return calendar
    
    def _get_companion_plants(self, crop_type: str) -> List[str]:
        """Get companion plants for the crop"""
        companions = {
            "tomato": ["basil", "carrots", "marigold", "nasturtium"],
            "potato": ["beans", "corn", "cabbage", "horseradish"],
            "corn": ["beans", "squash", "cucumber", "peas"],
            "wheat": ["legumes", "mustard", "flax"],
            "rice": ["azolla", "duckweed", "fish (aquaponics)"]
        }
        return companions.get(crop_type, ["marigold", "basil", "nasturtium"])
    
    def _get_common_mistakes(self, crop_type: str) -> List[str]:
        """Get common planting mistakes"""
        return [
            "Planting too early or late in season",
            "Overcrowding plants",
            "Planting in poorly drained soil",
            "Insufficient sunlight",
            "Overwatering or underwatering",
            "Ignoring soil pH requirements",
            "Not rotating crops"
        ]
    
    def _generate_planting_tips(self, crop_type: str, soil_type: str, season: str) -> List[str]:
        """Generate specific planting tips"""
        tips = [
            f"Test soil pH before planting {crop_type}",
            f"Ensure {soil_type} soil is well-prepared with organic matter",
            f"Monitor weather forecast for {season} planting",
            "Use quality seeds from reputable sources",
            "Consider succession planting for continuous harvest",
            "Install irrigation system before planting",
            "Plan for pest management strategies"
        ]
        return tips
    
    def _calculate_irrigation_need(self, soil_moisture: float, weather_data: Dict,
                                  growth_stage: str, crop_type: str) -> Dict:
        """Calculate irrigation requirements"""
        # Simple logic for demonstration
        if soil_moisture < 30:
            action = "Irrigate immediately"
            amount = "2-3 inches"
            frequency = "Daily until moisture improves"
        elif soil_moisture < 50:
            action = "Irrigate soon"
            amount = "1-2 inches"
            frequency = "Every 2-3 days"
        else:
            action = "Monitor closely"
            amount = "1 inch"
            frequency = "Weekly or as needed"
        
        return {
            "action": action,
            "amount": amount,
            "frequency": frequency,
            "method": "Drip irrigation recommended",
            "timing": "Early morning (6-8 AM) or evening (6-8 PM)"
        }
    
    def _generate_irrigation_schedule(self, crop_type: str, growth_stage: str,
                                     weather_data: Dict) -> List[Dict]:
        """Generate irrigation schedule"""
        schedule = []
        for i in range(7):
            date = datetime.now() + timedelta(days=i)
            schedule.append({
                "date": date.strftime("%Y-%m-%d"),
                "water_amount": "1 inch" if i % 3 == 0 else "0.5 inch",
                "time": "6:00 AM"
            })
        return schedule
    
    def _analyze_soil_test(self, soil_test_results: Dict) -> Dict:
        """Analyze soil test results"""
        # Simple analysis for demonstration
        health_score = random.randint(60, 95)
        
        return {
            "health_score": health_score,
            "status": "Good" if health_score > 75 else "Needs improvement",
            "nutrients": {
                "N": soil_test_results.get("nitrogen", "moderate"),
                "P": soil_test_results.get("phosphorus", "adequate"),
                "K": soil_test_results.get("potassium", "adequate")
            },
            "amendments": [
                "Add lime to raise pH" if soil_test_results.get("ph", 6.5) < 6 else None,
                "Add sulfur to lower pH" if soil_test_results.get("ph", 6.5) > 7.5 else None,
                "Add organic matter"
            ],
            "immediate_actions": ["Test water source", "Add compost"],
            "pre_planting": ["Apply lime/sulfur if needed", "Add base fertilizer"],
            "maintenance": ["Regular testing", "Mulching", "Cover crops"]
        }
    
    def _get_rotation_advice(self, current_crop: str, previous_crops: List[str]) -> Dict:
        """Get crop rotation advice"""
        rotation_groups = {
            "legumes": ["beans", "peas", "lentils"],
            "brassicas": ["cabbage", "broccoli", "cauliflower"],
            "nightshades": ["tomato", "potato", "pepper", "eggplant"],
            "grains": ["wheat", "corn", "rice", "barley"],
            "roots": ["carrot", "beet", "radish", "turnip"]
        }
        
        return {
            "current_crop": current_crop,
            "previous_crops": previous_crops,
            "recommended_next": ["legumes", "grains"] if current_crop in ["tomato", "potato"] else ["nightshades", "roots"],
            "avoid_next": ["nightshades"] if current_crop in ["tomato", "potato"] else [],
            "benefits": "Improves soil health, reduces disease, balances nutrients"
        }
    
    def _get_soil_amendments(self, soil_type: str, crop_type: str) -> List[str]:
        """Get soil amendments recommendations"""
        amendments = {
            "clay": ["organic matter", "sand", "gypsum", "compost"],
            "sandy": ["organic matter", "compost", "peat moss", "clay"],
            "loam": ["compost", "aged manure"],
            "silt": ["organic matter", "compost", "perlite"]
        }
        return amendments.get(soil_type, ["compost", "organic matter"])
    
    def _calculate_fertilizer_needs(self, crop_type: str, soil_data: Dict,
                                   growth_stage: str) -> Dict:
        """Calculate fertilizer requirements"""
        # Simplified calculation
        base_amount = "2-3 lbs per 100 sq ft"
        
        stage_multipliers = {
            "seedling": 0.5,
            "vegetative": 1.0,
            "flowering": 1.5,
            "fruiting": 1.2,
            "maturation": 0.3
        }
        
        multiplier = stage_multipliers.get(growth_stage, 1.0)
        
        return {
            "amount": base_amount,
            "method": "Side dressing" if growth_stage != "seedling" else "Broadcast",
            "micronutrients": ["calcium", "magnesium", "iron"],
            "stage_specific": f"Apply {multiplier}x normal rate for {growth_stage} stage",
            "deficiency_signs": {
                "nitrogen": "Yellow lower leaves",
                "phosphorus": "Purple leaves",
                "potassium": "Brown leaf edges"
            }
        }