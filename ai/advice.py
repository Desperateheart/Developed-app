from typing import Dict, Any, Optional, List
import json

try:
	from openai import OpenAI
except Exception:  # pragma: no cover
	OpenAI = None  # type: ignore


def _heuristic_advice(
	*,
	crop: str,
	soil_ph: float,
	irrigation_method: str,
	soil_moisture_pct: int,
	crop_stage: str,
	location_query: str,
	weather: Optional[Dict[str, Any]],
) -> Dict[str, Any]:
	key_recommendations: List[str] = []

	# pH guidance
	optimal_ph = {
		"Tomato": (6.0, 6.8),
		"Potato": (5.0, 6.0),
		"Wheat": (6.0, 7.5),
		"Rice": (5.5, 7.0),
		"Maize": (5.8, 7.2),
		"Cotton": (5.8, 8.0),
		"Soybean": (6.0, 7.5),
		"Cassava": (4.5, 7.0),
		"Banana": (5.5, 7.0),
		"Grape": (5.5, 7.0),
	}
	low, high = optimal_ph.get(crop, (5.8, 7.2))
	if soil_ph < low:
		key_recommendations.append(
			f"Soil pH ({soil_ph:.1f}) is low for {crop}. Consider liming to raise pH towards {low}-{high}."
		)
	elif soil_ph > high:
		key_recommendations.append(
			f"Soil pH ({soil_ph:.1f}) is high for {crop}. Apply elemental sulfur or acidifying fertilizers to reach {low}-{high}."
		)
	else:
		key_recommendations.append(f"Soil pH is within the optimal range {low}-{high} for {crop}.")

	# Moisture and irrigation
	if irrigation_method == "Rainfed":
		if weather and weather.get("forecast", {}).get("precip_next_24h_mm", 0) >= 10:
			key_recommendations.append("Significant rain expected; avoid irrigation for the next 24–48 hours.")
		elif soil_moisture_pct < 25:
			key_recommendations.append("Soil moisture is low; schedule irrigation within 24 hours if rain is not forecast.")
	else:
		if soil_moisture_pct < 30:
			key_recommendations.append(
				"Increase irrigation frequency slightly (shorter intervals). Monitor root-zone moisture."
			)
		elif soil_moisture_pct > 70:
			key_recommendations.append("Reduce irrigation to prevent waterlogging and disease risk.")

	# Crop stage specific
	if crop_stage == "Pre-planting":
		key_recommendations.append("Perform soil test; incorporate basal NPK and organic matter (compost or FYM).")
	elif crop_stage == "Vegetative":
		key_recommendations.append("Apply split nitrogen; maintain weed-free field and scout for pests weekly.")
	elif crop_stage == "Flowering":
		key_recommendations.append("Avoid water stress; ensure uniform soil moisture; protect against fungal diseases.")
	elif crop_stage == "Fruiting/Grain filling":
		key_recommendations.append("Maintain consistent moisture; apply K if deficiency symptoms appear.")
	elif crop_stage == "Maturity":
		key_recommendations.append("Reduce irrigation; prepare for timely harvest in dry windows.")

	irrigation_schedule = None
	if irrigation_method in ("Drip", "Sprinkler"):
		if crop_stage in ("Vegetative", "Flowering"):
			irrigation_schedule = "Irrigate lightly every 2–3 days; target 20–30 mm/week adjusted for rainfall."
		else:
			irrigation_schedule = "Irrigate every 4–5 days; avoid overwatering near maturity."
	elif irrigation_method == "Flood":
		irrigation_schedule = "Irrigate in longer intervals; avoid standing water for more than 24–48 hours."
	else:  # Rainfed
		irrigation_schedule = "Rely on rainfall; conserve moisture with mulch and timely weeding."

	return {
		"key_recommendations": key_recommendations,
		"irrigation_schedule": irrigation_schedule,
	}


def generate_farming_advice(
	*,
	crop: str,
	soil_ph: float,
	irrigation_method: str,
	soil_moisture_pct: int,
	crop_stage: str,
	location_query: str,
	weather: Optional[Dict[str, Any]],
	openai_api_key: Optional[str],
) -> Dict[str, Any]:
	if openai_api_key and OpenAI is not None:
		try:
			client = OpenAI(api_key=openai_api_key)
			system = (
				"You are a concise agronomy assistant. Provide actionable, localized advice for farmers. "
				"Focus on irrigation, soil, fertilization, and pest/disease prevention. Avoid brand names."
			)
			user_payload = {
				"crop": crop,
				"soil_ph": soil_ph,
				"irrigation_method": irrigation_method,
				"soil_moisture_pct": soil_moisture_pct,
				"crop_stage": crop_stage,
				"location": location_query,
				"weather": weather or {},
			}
			messages = [
				{"role": "system", "content": system},
				{"role": "user", "content": f"Return JSON with keys: key_recommendations (array), irrigation_schedule (string). Context: {json.dumps(user_payload)}"},
			]
			response = client.chat.completions.create(
				model="gpt-4o-mini",
				messages=messages,
				temperature=0.2,
			)
			text = response.choices[0].message.content or "{}"
			try:
				return json.loads(text)
			except Exception:
				start = text.find("{")
				end = text.rfind("}")
				return json.loads(text[start : end + 1]) if start != -1 and end != -1 else _heuristic_advice(
					crop=crop,
					soil_ph=soil_ph,
					irrigation_method=irrigation_method,
					soil_moisture_pct=soil_moisture_pct,
					crop_stage=crop_stage,
					location_query=location_query,
					weather=weather,
				)
		except Exception as e:
			return _heuristic_advice(
				crop=crop,
				soil_ph=soil_ph,
				irrigation_method=irrigation_method,
				soil_moisture_pct=soil_moisture_pct,
				crop_stage=crop_stage,
				location_query=location_query,
				weather=weather,
			) | {"note": f"LLM unavailable: {e}"}
	else:
		return _heuristic_advice(
			crop=crop,
			soil_ph=soil_ph,
			irrigation_method=irrigation_method,
			soil_moisture_pct=soil_moisture_pct,
			crop_stage=crop_stage,
			location_query=location_query,
			weather=weather,
		)