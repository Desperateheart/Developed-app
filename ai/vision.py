import base64
import io
import json
import os
from typing import Dict, Any, Optional, List

from PIL import Image

try:
	from openai import OpenAI
except Exception:  # pragma: no cover
	OpenAI = None  # type: ignore


def _encode_image_to_base64(image_bytes: bytes) -> str:
	return base64.b64encode(image_bytes).decode("utf-8")


def _heuristic_leaf_analysis(image_bytes: bytes, crop: Optional[str]) -> Dict[str, Any]:
	image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
	width, height = image.size
	pixels = list(image.getdata())
	total = len(pixels)

	greenish = 0
	yellowish = 0
	brownish = 0
	dark_spots = 0

	for (r, g, b) in pixels[:: max(1, total // 50000)]:  # sample if very large
		if g > r and g > b and g > 90:
			greenish += 1
		elif r > 120 and g > 120 and b < 90:
			yellowish += 1
		elif r > 90 and g < 80 and b < 80:
			brownish += 1
		if r < 50 and g < 50 and b < 50:
			dark_spots += 1

	green_ratio = greenish / (total or 1)
	yellow_ratio = yellowish / (total or 1)
	brown_ratio = brownish / (total or 1)
	dark_ratio = dark_spots / (total or 1)

	# Naive rules
	if brown_ratio > 0.15 and dark_ratio > 0.03:
		disease = "Leaf blight"
		desc = "Irregular brown lesions with darker necrotic centers; potential blight."
		actions = [
			"Remove and destroy heavily infected leaves",
			"Avoid overhead irrigation; prefer drip",
			"Apply recommended copper-based fungicide following label",
		]
		confidence = min(0.9, 0.5 + brown_ratio)
	elif yellow_ratio > 0.15 and green_ratio < 0.6:
		disease = "Nutrient deficiency / Chlorosis"
		desc = "Widespread yellowing suggests chlorosis, often due to N deficiency or iron lockout (pH)."
		actions = [
			"Soil test for N and Fe; correct pH to crop-optimal",
			"Apply balanced N fertilizer split over 2-3 doses",
			"Mulch to conserve moisture",
		]
		confidence = min(0.8, 0.4 + yellow_ratio)
	else:
		disease = "Rust / Spotting (suspected)"
		desc = "Scattered darker pustules or spots visible; could indicate rust or early spot diseases."
		actions = [
			"Improve field airflow; avoid leaf wetness",
			"Scout regularly; apply fungicide if spread increases",
		]
		confidence = 0.55

	return {
		"disease_name": disease,
		"crop": crop or "Unknown",
		"confidence": confidence,
		"description": desc,
		"recommended_actions": actions,
	}


def detect_disease_from_image(image_bytes: bytes, crop: Optional[str], openai_api_key: Optional[str]) -> Dict[str, Any]:
	if openai_api_key and OpenAI is not None:
		try:
			client = OpenAI(api_key=openai_api_key)
			b64 = _encode_image_to_base64(image_bytes)
			prompt = (
				"You are an agronomy vision expert. Identify likely crop disease from the image. "
				"If multiple, choose the most probable. Output concise JSON with keys: "
				"disease_name, crop, confidence (0..1), description, recommended_actions (array). "
				f"Assume crop: {crop if crop else 'Unknown'}."
			)
			messages = [
				{
					"role": "user",
					"content": [
						{"type": "text", "text": prompt},
						{
							"type": "image_url",
							"image_url": {"url": f"data:image/jpeg;base64,{b64}"},
						},
					],
				}
			]
			response = client.chat.completions.create(
				model="gpt-4o-mini",
				messages=messages,
				temperature=0.2,
			)
			text = response.choices[0].message.content or "{}"
			try:
				parsed = json.loads(text)
			except Exception:
				# attempt to extract JSON substring
				start = text.find("{")
				end = text.rfind("}")
				parsed = json.loads(text[start : end + 1]) if start != -1 and end != -1 else {}

			# Normalize fields
			parsed.setdefault("crop", crop or "Unknown")
			if isinstance(parsed.get("recommended_actions"), str):
				parsed["recommended_actions"] = [parsed["recommended_actions"]]
			if parsed.get("confidence") is None:
				parsed["confidence"] = 0.7
			return parsed
		except Exception as e:  # Fall back to heuristic
			return _heuristic_leaf_analysis(image_bytes=image_bytes, crop=crop) | {"note": f"LLM unavailable: {e}"}
	else:
		return _heuristic_leaf_analysis(image_bytes=image_bytes, crop=crop)