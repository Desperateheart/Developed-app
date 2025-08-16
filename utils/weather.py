from typing import Dict, Any
import requests


def get_weather_for_location(*, latitude: float, longitude: float) -> Dict[str, Any]:
	params = {
		"latitude": latitude,
		"longitude": longitude,
		"hourly": "precipitation,temperature_2m,soil_moisture_0_1cm",
		"daily": "temperature_2m_max,temperature_2m_min,precipitation_sum",
		"current_weather": True,
		"timezone": "auto",
	}
	resp = requests.get("https://api.open-meteo.com/v1/forecast", params=params, timeout=20)
	resp.raise_for_status()
	data = resp.json()

	current = data.get("current_weather", {})
	hourly = data.get("hourly", {})
	forecast_precip_next_24h = 0.0
	if hourly:
		precip = hourly.get("precipitation", [])
		forecast_precip_next_24h = float(sum(precip[:24])) if precip else 0.0

	return {
		"current": {
			"temperature_c": current.get("temperature"),
			"windspeed_kmh": current.get("windspeed"),
			"weathercode": current.get("weathercode"),
		},
		"forecast": {
			"precip_next_24h_mm": forecast_precip_next_24h,
			"tmax_c": (data.get("daily", {}).get("temperature_2m_max") or [None])[0],
			"tmin_c": (data.get("daily", {}).get("temperature_2m_min") or [None])[0],
		},
	}