from typing import Dict, Any, List
import json
import os

_DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")


def _load_json(path: str):
	with open(path, "r", encoding="utf-8") as f:
		return json.load(f)


def load_price_dataset() -> List[Dict[str, Any]]:
	path = os.path.join(_DATA_DIR, "prices.json")
	return _load_json(path)


def load_buyer_directory() -> List[Dict[str, Any]]:
	path = os.path.join(_DATA_DIR, "buyers.json")
	return _load_json(path)


def suggest_fair_price(*, crop: str, region: str, quantity_tonnes: float) -> Dict[str, Any]:
	prices = load_price_dataset()
	region_match = None
	national_match = None
	for row in prices:
		if row["crop"].lower() == crop.lower():
			if row["region"].lower() in region:
				region_match = row
			elif row.get("region_scope") == "national" and (national_match is None):
				national_match = row

	ref = region_match or national_match
	if not ref:
		ref = {"currency": "USD", "price_per_tonne": 300.0, "low": 250.0, "high": 350.0}
	
	currency = ref.get("currency", "USD")
	median = float(ref.get("price_per_tonne", 300.0))
	low = float(ref.get("low", median * 0.9))
	high = float(ref.get("high", median * 1.1))

	return {
		"currency": currency,
		"fair_price_per_tonne": median,
		"low_per_tonne": low,
		"high_per_tonne": high,
		"estimated_total": median * max(0.0, quantity_tonnes),
	}


def find_buyers(*, crop: str, region: str) -> List[Dict[str, Any]]:
	buyers = load_buyer_directory()
	crop = crop.lower()
	region = region.lower()
	local = [b for b in buyers if crop in [c.lower() for c in b.get("crops", [])] and b.get("region", "").lower() in region]
	if local:
		return local
	# fall back to national/international buyers for the crop
	return [b for b in buyers if crop in [c.lower() for c in b.get("crops", [])] and b.get("region_scope") in ("national", "international")]