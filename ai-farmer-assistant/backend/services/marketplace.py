from typing import Dict, List, Optional
from datetime import datetime, timedelta
import random
import json

class MarketplaceService:
    """
    Service for marketplace features including price suggestions and buyer connections
    """
    
    def __init__(self):
        # Mock market data - in production, this would come from real market APIs
        self.market_prices = {
            "tomato": {
                "base_price": 2.50,  # per kg
                "quality_multipliers": {
                    "A": 1.3,
                    "B": 1.0,
                    "C": 0.7
                },
                "seasonal_factors": {
                    "spring": 1.1,
                    "summer": 0.9,
                    "fall": 1.2,
                    "winter": 1.4
                }
            },
            "potato": {
                "base_price": 1.80,
                "quality_multipliers": {
                    "A": 1.25,
                    "B": 1.0,
                    "C": 0.75
                }
            },
            "wheat": {
                "base_price": 0.35,  # per kg
                "quality_multipliers": {
                    "A": 1.2,
                    "B": 1.0,
                    "C": 0.8
                }
            },
            "rice": {
                "base_price": 0.85,
                "quality_multipliers": {
                    "A": 1.35,
                    "B": 1.0,
                    "C": 0.70
                }
            },
            "corn": {
                "base_price": 0.28,
                "quality_multipliers": {
                    "A": 1.15,
                    "B": 1.0,
                    "C": 0.85
                }
            }
        }
        
        # Mock buyer database
        self.buyers_database = [
            {
                "id": 1,
                "name": "Fresh Mart Supermarket",
                "type": "Retail Chain",
                "location": "New York",
                "preferred_crops": ["tomato", "potato", "corn"],
                "min_quantity": 100,
                "max_quantity": 5000,
                "quality_requirements": ["A", "B"],
                "payment_terms": "Net 30 days",
                "contact": "+1-555-0101",
                "email": "procurement@freshmart.com",
                "rating": 4.5,
                "verified": True
            },
            {
                "id": 2,
                "name": "Green Valley Distributors",
                "type": "Wholesale",
                "location": "California",
                "preferred_crops": ["tomato", "potato", "corn", "wheat"],
                "min_quantity": 500,
                "max_quantity": 10000,
                "quality_requirements": ["A", "B"],
                "payment_terms": "Net 15 days",
                "contact": "+1-555-0102",
                "email": "orders@greenvalley.com",
                "rating": 4.8,
                "verified": True
            },
            {
                "id": 3,
                "name": "Farm to Table Restaurant Group",
                "type": "Restaurant",
                "location": "Chicago",
                "preferred_crops": ["tomato", "potato", "corn"],
                "min_quantity": 50,
                "max_quantity": 500,
                "quality_requirements": ["A"],
                "payment_terms": "Cash on delivery",
                "contact": "+1-555-0103",
                "email": "chef@farmtotable.com",
                "rating": 4.7,
                "verified": True
            },
            {
                "id": 4,
                "name": "Global Grain Traders",
                "type": "Export",
                "location": "Texas",
                "preferred_crops": ["wheat", "rice", "corn"],
                "min_quantity": 1000,
                "max_quantity": 50000,
                "quality_requirements": ["A", "B", "C"],
                "payment_terms": "Letter of Credit",
                "contact": "+1-555-0104",
                "email": "trading@globalgraintraders.com",
                "rating": 4.3,
                "verified": True
            },
            {
                "id": 5,
                "name": "Local Farmers Market",
                "type": "Direct Sale",
                "location": "Various",
                "preferred_crops": ["all"],
                "min_quantity": 10,
                "max_quantity": 200,
                "quality_requirements": ["A", "B", "C"],
                "payment_terms": "Cash",
                "contact": "+1-555-0105",
                "email": "info@localfarmersmarket.com",
                "rating": 4.6,
                "verified": False
            }
        ]
        
        self.active_listings = []
    
    async def get_market_prices(self, crop_type: str, location: Optional[str] = None,
                                quality_grade: Optional[str] = None) -> Dict:
        """
        Get current market prices for crops
        """
        crop_type = crop_type.lower()
        base_data = self.market_prices.get(crop_type, self.market_prices["tomato"])
        
        # Calculate price based on various factors
        base_price = base_data["base_price"]
        
        # Apply quality multiplier
        if quality_grade:
            quality_mult = base_data["quality_multipliers"].get(quality_grade.upper(), 1.0)
            base_price *= quality_mult
        
        # Add some random market fluctuation
        market_fluctuation = random.uniform(0.9, 1.1)
        current_price = base_price * market_fluctuation
        
        # Generate price history
        price_history = self._generate_price_history(base_price, 30)
        
        # Calculate price trends
        trend = "stable"
        if price_history[-1] > price_history[-7]:
            trend = "increasing"
        elif price_history[-1] < price_history[-7]:
            trend = "decreasing"
        
        return {
            "crop": crop_type,
            "location": location or "National Average",
            "current_price": {
                "value": round(current_price, 2),
                "unit": "$/kg",
                "quality_grade": quality_grade or "B",
                "timestamp": datetime.now().isoformat()
            },
            "price_range": {
                "min": round(base_price * 0.7, 2),
                "max": round(base_price * 1.3, 2),
                "average": round(base_price, 2)
            },
            "trend": trend,
            "price_history": price_history,
            "market_factors": {
                "supply": "moderate",
                "demand": "high" if trend == "increasing" else "moderate",
                "seasonal_impact": self._get_seasonal_impact(crop_type),
                "weather_impact": "neutral"
            },
            "forecast": {
                "next_week": round(current_price * random.uniform(0.95, 1.05), 2),
                "next_month": round(current_price * random.uniform(0.9, 1.1), 2),
                "confidence": "moderate"
            },
            "comparison": {
                "vs_last_week": f"{random.choice(['+', '-'])}{random.randint(1, 10)}%",
                "vs_last_month": f"{random.choice(['+', '-'])}{random.randint(5, 15)}%",
                "vs_last_year": f"{random.choice(['+', '-'])}{random.randint(10, 25)}%"
            }
        }
    
    async def suggest_fair_price(self, crop_type: str, quantity: float,
                                quality_metrics: Dict, location: str) -> Dict:
        """
        Suggest fair price based on quality, quantity, and market conditions
        """
        crop_type = crop_type.lower()
        base_data = self.market_prices.get(crop_type, self.market_prices["tomato"])
        
        # Start with base price
        base_price = base_data["base_price"]
        
        # Determine quality grade from metrics
        quality_grade = self._determine_quality_grade(quality_metrics)
        quality_mult = base_data["quality_multipliers"].get(quality_grade, 1.0)
        
        # Apply quantity discount/premium
        quantity_factor = self._calculate_quantity_factor(quantity)
        
        # Location factor (simplified)
        location_factor = 1.0
        if "urban" in location.lower() or "city" in location.lower():
            location_factor = 1.15
        elif "rural" in location.lower():
            location_factor = 0.95
        
        # Calculate suggested price
        suggested_price = base_price * quality_mult * quantity_factor * location_factor
        
        # Add market intelligence
        competitors = self._get_competitor_prices(crop_type, quality_grade, location)
        
        return {
            "crop": crop_type,
            "quantity": f"{quantity} kg",
            "quality_grade": quality_grade,
            "location": location,
            "suggested_price": {
                "per_kg": round(suggested_price, 2),
                "total": round(suggested_price * quantity, 2),
                "currency": "USD"
            },
            "price_breakdown": {
                "base_price": round(base_price, 2),
                "quality_adjustment": f"{round((quality_mult - 1) * 100, 1)}%",
                "quantity_adjustment": f"{round((quantity_factor - 1) * 100, 1)}%",
                "location_adjustment": f"{round((location_factor - 1) * 100, 1)}%"
            },
            "market_comparison": {
                "vs_market_average": round(suggested_price - base_price, 2),
                "percentile": random.randint(40, 80),
                "competitor_prices": competitors
            },
            "negotiation_range": {
                "minimum": round(suggested_price * 0.9, 2),
                "target": round(suggested_price, 2),
                "maximum": round(suggested_price * 1.1, 2)
            },
            "selling_tips": [
                "Highlight the quality grade of your produce",
                "Consider offering bulk discounts for large orders",
                "Provide samples to potential buyers",
                "Maintain consistent quality across batches",
                "Build long-term relationships with buyers"
            ],
            "best_time_to_sell": self._get_best_selling_time(crop_type),
            "confidence_score": random.randint(75, 95)
        }
    
    async def find_buyers(self, crop_type: str, location: str,
                         quantity: float, delivery_date: Optional[str] = None) -> Dict:
        """
        Find potential buyers for crops
        """
        crop_type = crop_type.lower()
        
        # Filter buyers based on criteria
        matching_buyers = []
        for buyer in self.buyers_database:
            if (crop_type in buyer["preferred_crops"] or "all" in buyer["preferred_crops"]) and \
               buyer["min_quantity"] <= quantity <= buyer["max_quantity"]:
                # Calculate match score
                match_score = self._calculate_buyer_match_score(
                    buyer, crop_type, location, quantity
                )
                buyer_info = buyer.copy()
                buyer_info["match_score"] = match_score
                matching_buyers.append(buyer_info)
        
        # Sort by match score
        matching_buyers.sort(key=lambda x: x["match_score"], reverse=True)
        
        # Get market insights
        market_insights = self._get_market_insights(crop_type, location)
        
        return {
            "search_criteria": {
                "crop": crop_type,
                "location": location,
                "quantity": f"{quantity} kg",
                "delivery_date": delivery_date or "Flexible"
            },
            "buyers_found": len(matching_buyers),
            "matching_buyers": matching_buyers[:10],  # Top 10 matches
            "buyer_categories": {
                "retail": len([b for b in matching_buyers if b["type"] == "Retail Chain"]),
                "wholesale": len([b for b in matching_buyers if b["type"] == "Wholesale"]),
                "export": len([b for b in matching_buyers if b["type"] == "Export"]),
                "direct": len([b for b in matching_buyers if b["type"] == "Direct Sale"])
            },
            "market_insights": market_insights,
            "connection_tips": [
                "Prepare product samples and quality certificates",
                "Be ready to negotiate on price and delivery terms",
                "Maintain communication throughout the process",
                "Consider starting with smaller trial orders",
                "Get agreements in writing"
            ],
            "recommended_actions": self._get_recommended_actions(matching_buyers)
        }
    
    async def create_listing(self, seller_id: int, crop_type: str, quantity: float,
                           price: float, location: str, harvest_date: str,
                           description: str) -> Dict:
        """
        Create a new marketplace listing
        """
        listing = {
            "id": len(self.active_listings) + 1,
            "seller_id": seller_id,
            "crop_type": crop_type,
            "quantity": quantity,
            "price_per_kg": price,
            "total_value": quantity * price,
            "location": location,
            "harvest_date": harvest_date,
            "listing_date": datetime.now().isoformat(),
            "expiry_date": (datetime.now() + timedelta(days=30)).isoformat(),
            "description": description,
            "status": "active",
            "views": 0,
            "inquiries": 0,
            "quality_certification": "pending",
            "images": []
        }
        
        self.active_listings.append(listing)
        
        # Generate listing insights
        market_position = self._analyze_listing_position(listing)
        
        return {
            "listing": listing,
            "success": True,
            "message": "Listing created successfully",
            "listing_url": f"/marketplace/listing/{listing['id']}",
            "market_position": market_position,
            "optimization_tips": [
                "Add high-quality photos of your produce",
                "Include quality certifications if available",
                "Respond to inquiries within 24 hours",
                "Consider competitive pricing based on market rates",
                "Update listing if harvest date changes"
            ],
            "estimated_visibility": {
                "daily_views": random.randint(20, 100),
                "expected_inquiries": random.randint(5, 20),
                "conversion_rate": f"{random.randint(10, 30)}%"
            }
        }
    
    async def get_listings(self, crop_type: Optional[str] = None,
                          location: Optional[str] = None,
                          min_quantity: Optional[float] = None,
                          max_price: Optional[float] = None) -> List[Dict]:
        """
        Get marketplace listings with filters
        """
        # Filter listings based on criteria
        filtered_listings = self.active_listings.copy()
        
        if crop_type:
            filtered_listings = [l for l in filtered_listings 
                                if l["crop_type"].lower() == crop_type.lower()]
        
        if location:
            filtered_listings = [l for l in filtered_listings 
                                if location.lower() in l["location"].lower()]
        
        if min_quantity:
            filtered_listings = [l for l in filtered_listings 
                                if l["quantity"] >= min_quantity]
        
        if max_price:
            filtered_listings = [l for l in filtered_listings 
                                if l["price_per_kg"] <= max_price]
        
        # Add some mock listings if empty
        if not filtered_listings:
            filtered_listings = self._generate_mock_listings(crop_type, location)
        
        return {
            "total_listings": len(filtered_listings),
            "filters_applied": {
                "crop_type": crop_type,
                "location": location,
                "min_quantity": min_quantity,
                "max_price": max_price
            },
            "listings": filtered_listings[:20],  # Paginate to 20 results
            "summary_stats": {
                "average_price": self._calculate_average_price(filtered_listings),
                "total_quantity": sum(l["quantity"] for l in filtered_listings),
                "price_range": self._get_price_range(filtered_listings)
            }
        }
    
    async def get_market_trends(self, crop_type: str, period: str = "monthly") -> Dict:
        """
        Get market trend analytics
        """
        crop_type = crop_type.lower()
        
        # Generate trend data based on period
        if period == "daily":
            data_points = 7
        elif period == "weekly":
            data_points = 4
        elif period == "monthly":
            data_points = 12
        else:
            data_points = 12
        
        # Generate mock trend data
        base_price = self.market_prices.get(crop_type, self.market_prices["tomato"])["base_price"]
        price_trend = self._generate_price_history(base_price, data_points)
        volume_trend = [random.randint(1000, 5000) for _ in range(data_points)]
        
        # Calculate statistics
        price_change = ((price_trend[-1] - price_trend[0]) / price_trend[0]) * 100
        volume_change = ((volume_trend[-1] - volume_trend[0]) / volume_trend[0]) * 100
        
        return {
            "crop": crop_type,
            "period": period,
            "price_trends": {
                "data": price_trend,
                "change_percentage": round(price_change, 2),
                "trend_direction": "up" if price_change > 0 else "down",
                "volatility": "moderate"
            },
            "volume_trends": {
                "data": volume_trend,
                "change_percentage": round(volume_change, 2),
                "peak_season": self._get_peak_season(crop_type)
            },
            "market_indicators": {
                "supply_index": random.randint(60, 90),
                "demand_index": random.randint(70, 95),
                "price_stability": random.randint(65, 85),
                "market_sentiment": random.choice(["bullish", "neutral", "bearish"])
            },
            "top_regions": [
                {"region": "California", "volume": random.randint(5000, 10000)},
                {"region": "Texas", "volume": random.randint(4000, 8000)},
                {"region": "Florida", "volume": random.randint(3000, 7000)}
            ],
            "forecast": {
                "next_period_price": round(price_trend[-1] * random.uniform(0.95, 1.05), 2),
                "confidence": f"{random.randint(70, 90)}%",
                "factors": [
                    "Seasonal patterns",
                    "Weather conditions",
                    "Market demand",
                    "Supply chain factors"
                ]
            },
            "recommendations": [
                "Consider forward contracts at current prices" if price_change > 5 else "Wait for better prices",
                "Diversify buyer base",
                "Monitor competitor pricing",
                "Plan harvest timing for peak demand"
            ]
        }
    
    # Helper methods
    def _generate_price_history(self, base_price: float, days: int) -> List[float]:
        """Generate historical price data"""
        prices = []
        current_price = base_price
        
        for _ in range(days):
            # Random walk with mean reversion
            change = random.uniform(-0.1, 0.1)
            current_price = current_price * (1 + change)
            # Mean reversion
            current_price = 0.9 * current_price + 0.1 * base_price
            prices.append(round(current_price, 2))
        
        return prices
    
    def _get_seasonal_impact(self, crop_type: str) -> str:
        """Get seasonal impact on prices"""
        season_impacts = {
            "tomato": "High demand in summer, prices peak in winter",
            "potato": "Stable year-round with slight increase in fall",
            "wheat": "Harvest season brings lower prices",
            "rice": "Monsoon affects supply and prices",
            "corn": "Peak prices before harvest season"
        }
        return season_impacts.get(crop_type, "Moderate seasonal variation")
    
    def _determine_quality_grade(self, quality_metrics: Dict) -> str:
        """Determine quality grade from metrics"""
        # Simple scoring system
        score = 0
        
        if quality_metrics.get("size", "medium") == "large":
            score += 30
        elif quality_metrics.get("size", "medium") == "medium":
            score += 20
        
        if quality_metrics.get("appearance", "good") == "excellent":
            score += 30
        elif quality_metrics.get("appearance", "good") == "good":
            score += 20
        
        if quality_metrics.get("freshness", "fresh") == "very fresh":
            score += 25
        elif quality_metrics.get("freshness", "fresh") == "fresh":
            score += 15
        
        if quality_metrics.get("defects", 5) < 2:
            score += 15
        elif quality_metrics.get("defects", 5) < 5:
            score += 10
        
        if score >= 80:
            return "A"
        elif score >= 50:
            return "B"
        else:
            return "C"
    
    def _calculate_quantity_factor(self, quantity: float) -> float:
        """Calculate price factor based on quantity"""
        if quantity < 50:
            return 1.1  # Small quantity premium
        elif quantity < 500:
            return 1.0  # Standard price
        elif quantity < 5000:
            return 0.95  # Bulk discount
        else:
            return 0.9  # Large bulk discount
    
    def _get_competitor_prices(self, crop_type: str, quality_grade: str,
                               location: str) -> List[Dict]:
        """Get competitor price information"""
        base_price = self.market_prices.get(crop_type, self.market_prices["tomato"])["base_price"]
        quality_mult = self.market_prices.get(crop_type, self.market_prices["tomato"])["quality_multipliers"].get(quality_grade, 1.0)
        
        competitors = []
        for i in range(3):
            competitors.append({
                "seller": f"Competitor {i+1}",
                "price": round(base_price * quality_mult * random.uniform(0.9, 1.1), 2),
                "quality": quality_grade,
                "distance": f"{random.randint(5, 50)} km"
            })
        
        return competitors
    
    def _get_best_selling_time(self, crop_type: str) -> Dict:
        """Get best time to sell recommendations"""
        return {
            "immediate": "Good - Current prices are favorable",
            "this_week": "Prices expected to remain stable",
            "this_month": "Consider waiting if storage available",
            "seasonal_peak": self._get_peak_season(crop_type)
        }
    
    def _get_peak_season(self, crop_type: str) -> str:
        """Get peak season for crop"""
        peak_seasons = {
            "tomato": "Winter (December-February)",
            "potato": "Fall (September-November)",
            "wheat": "Post-harvest (June-August)",
            "rice": "Post-monsoon (October-December)",
            "corn": "Fall (September-October)"
        }
        return peak_seasons.get(crop_type, "Varies by region")
    
    def _calculate_buyer_match_score(self, buyer: Dict, crop_type: str,
                                    location: str, quantity: float) -> int:
        """Calculate match score between buyer and seller"""
        score = 0
        
        # Crop type match
        if crop_type in buyer["preferred_crops"] or "all" in buyer["preferred_crops"]:
            score += 30
        
        # Quantity match
        if buyer["min_quantity"] <= quantity <= buyer["max_quantity"]:
            score += 25
        
        # Location proximity (simplified)
        if buyer["location"].lower() in location.lower() or location.lower() in buyer["location"].lower():
            score += 20
        
        # Buyer rating
        score += int(buyer["rating"] * 5)
        
        # Verified buyer bonus
        if buyer["verified"]:
            score += 10
        
        return score
    
    def _get_market_insights(self, crop_type: str, location: str) -> Dict:
        """Get market insights for the crop and location"""
        return {
            "demand_level": random.choice(["High", "Moderate", "Low"]),
            "competition_level": random.choice(["High", "Moderate", "Low"]),
            "price_trend": random.choice(["Increasing", "Stable", "Decreasing"]),
            "best_buyers": ["Wholesale markets", "Retail chains", "Export markets"],
            "challenges": [
                "Price volatility",
                "Storage requirements",
                "Transportation costs"
            ],
            "opportunities": [
                "Direct sales to consumers",
                "Contract farming",
                "Value addition through processing"
            ]
        }
    
    def _get_recommended_actions(self, matching_buyers: List[Dict]) -> List[str]:
        """Get recommended actions based on buyer matches"""
        actions = []
        
        if len(matching_buyers) > 5:
            actions.append("Contact top 3 matched buyers first")
        
        if any(b["type"] == "Export" for b in matching_buyers[:5]):
            actions.append("Prepare export quality certification")
        
        if any(b["verified"] for b in matching_buyers[:3]):
            actions.append("Prioritize verified buyers for secure transactions")
        
        actions.extend([
            "Prepare product samples",
            "Document quality metrics",
            "Be flexible on delivery terms"
        ])
        
        return actions
    
    def _analyze_listing_position(self, listing: Dict) -> Dict:
        """Analyze how the listing compares to market"""
        crop_type = listing["crop_type"].lower()
        base_price = self.market_prices.get(crop_type, self.market_prices["tomato"])["base_price"]
        
        price_comparison = "competitive"
        if listing["price_per_kg"] < base_price * 0.9:
            price_comparison = "below market"
        elif listing["price_per_kg"] > base_price * 1.1:
            price_comparison = "above market"
        
        return {
            "price_position": price_comparison,
            "competitiveness_score": random.randint(60, 90),
            "visibility_score": random.randint(50, 85),
            "suggestions": [
                "Adjust price to market rate" if price_comparison != "competitive" else "Price is competitive",
                "Add quality certifications",
                "Include delivery options"
            ]
        }
    
    def _generate_mock_listings(self, crop_type: Optional[str],
                               location: Optional[str]) -> List[Dict]:
        """Generate mock listings for demonstration"""
        mock_listings = []
        crops = [crop_type] if crop_type else ["tomato", "potato", "wheat", "rice", "corn"]
        
        for i in range(5):
            crop = random.choice(crops)
            base_price = self.market_prices.get(crop.lower(), self.market_prices["tomato"])["base_price"]
            
            mock_listings.append({
                "id": 1000 + i,
                "seller_id": random.randint(100, 999),
                "crop_type": crop,
                "quantity": random.randint(100, 5000),
                "price_per_kg": round(base_price * random.uniform(0.8, 1.2), 2),
                "location": location or random.choice(["California", "Texas", "Florida"]),
                "harvest_date": (datetime.now() + timedelta(days=random.randint(1, 30))).isoformat(),
                "listing_date": (datetime.now() - timedelta(days=random.randint(1, 10))).isoformat(),
                "status": "active",
                "quality_grade": random.choice(["A", "B", "C"]),
                "views": random.randint(10, 200),
                "inquiries": random.randint(0, 20)
            })
        
        return mock_listings
    
    def _calculate_average_price(self, listings: List[Dict]) -> float:
        """Calculate average price from listings"""
        if not listings:
            return 0.0
        
        total_price = sum(l.get("price_per_kg", 0) for l in listings)
        return round(total_price / len(listings), 2)
    
    def _get_price_range(self, listings: List[Dict]) -> Dict:
        """Get price range from listings"""
        if not listings:
            return {"min": 0, "max": 0}
        
        prices = [l.get("price_per_kg", 0) for l in listings]
        return {
            "min": min(prices),
            "max": max(prices)
        }