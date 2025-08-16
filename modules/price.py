"""Price suggestion module (stub).

In a real deployment, you would integrate with market price APIs or databases.
Here we provide a simple heuristic based on base prices and quantity discounts.
"""

from typing import Optional, Dict, Any, List

# Base prices in USD per kg for demonstration
BASE_PRICES = {
    "maize": 0.25,
    "wheat": 0.30,
    "rice": 0.40,
    "soybean": 0.50,
    "cotton": 0.60,
}

# Dummy buyers database
BUYERS: List[Dict[str, str]] = [
    {"name": "AgriFoods Ltd.", "contact": "+1-555-0100"},
    {"name": "GreenMarket Co.", "contact": "+1-555-0200"},
    {"name": "Farmers Hub", "contact": "+1-555-0300"},
]


def calculate_price(crop: str, quantity: float) -> float:
    """Heuristic price calculation with quantity discount."""
    base_price = BASE_PRICES[crop]
    # Simple discount: 5% off for > 1000kg, 10% off for > 5000kg
    discount = 0.0
    if quantity > 5000:
        discount = 0.10
    elif quantity > 1000:
        discount = 0.05
    return base_price * (1 - discount)


def get_price_suggestion(crop: str, quantity: float) -> Optional[Dict[str, Any]]:
    crop_key = crop.lower().strip()
    if crop_key not in BASE_PRICES:
        return None

    unit_price = calculate_price(crop_key, quantity)
    total_price = unit_price * quantity

    # Return top 2 buyers for simplicity
    buyers = BUYERS[:2]

    return {
        "crop": crop_key,
        "quantity_kg": quantity,
        "unit_price_usd": round(unit_price, 2),
        "total_price_usd": round(total_price, 2),
        "prospective_buyers": buyers,
    }