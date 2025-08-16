"""Farming advice module.
Provides simple rule-based advice messages for common farming topics.
In production, you could integrate with agronomy databases or generative AI.
"""

from typing import Optional


ADVICE_DB: dict[str, str] = {
    "planting": (
        "Ensure the soil temperature is suitable before planting. Use certified seeds and plant at the recommended depth and spacing to optimize yield."
    ),
    "soil": (
        "Test your soil regularly to monitor pH and nutrient levels. Incorporate organic matter and consider crop rotation to maintain soil health."
    ),
    "irrigation": (
        "Irrigate early in the morning or late in the evening to minimize evaporation. Use drip irrigation where possible to conserve water."
    ),
    "fertilizer": (
        "Apply fertilizers based on soil test recommendations. Avoid over-fertilization which can harm crops and the environment."
    ),
    "pest": (
        "Monitor fields frequently for pests. Use integrated pest management techniques and avoid unnecessary pesticide applications."
    ),
}


def get_farming_advice(topic: str) -> Optional[str]:
    """Return advice for a given topic (case-insensitive)."""
    key = topic.lower().strip()
    return ADVICE_DB.get(key)