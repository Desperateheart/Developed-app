from typing import Optional, Dict
import requests


def geocode_location_to_coords(query: str) -> Optional[Dict[str, float]]:
	if not query:
		return None
	resp = requests.get(
		"https://geocoding-api.open-meteo.com/v1/search",
		params={"name": query, "count": 1, "language": "en", "format": "json"},
		timeout=20,
	)
	if resp.status_code != 200:
		return None
	data = resp.json()
	results = data.get("results") or []
	if not results:
		return None
	it = results[0]
	return {
		"latitude": float(it.get("latitude")),
		"longitude": float(it.get("longitude")),
		"name": it.get("name"),
		"country": it.get("country"),
		"admin1": it.get("admin1"),
	}


def normalize_region_name(region: str) -> str:
	return (region or "").strip().lower()