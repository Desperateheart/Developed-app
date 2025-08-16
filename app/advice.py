from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
import httpx
from datetime import datetime

router = APIRouter()


class AdviceRequest(BaseModel):
    crop: str = Field(..., description="Crop name, e.g., tomato, potato, maize, wheat, rice")
    growth_stage: str = Field(..., description="Stage: nursery, vegetative, flowering, fruiting, maturity")
    area_m2: float = Field(50.0, description="Cultivated area in square meters")
    soil_type: Optional[str] = Field(None, description="loam, sand, clay, silt")
    soil_ph: Optional[float] = Field(None)
    soil_moisture_pct: Optional[float] = Field(None, description="Volumetric water content percent")
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class AdviceResponse(BaseModel):
    irrigation: Dict[str, Any]
    planting: Dict[str, Any]
    soil: Dict[str, Any]
    notes: Optional[str] = None


_CROP_INFO = {
    "tomato": {
        "ph_range": (6.0, 6.8),
        "kc": {"nursery": 0.6, "vegetative": 0.95, "flowering": 1.05, "fruiting": 1.1, "maturity": 0.9},
        "temp_range_c": (18, 28),
        "npk_per_m2": {"vegetative": (0.8, 0.4, 0.6)},
    },
    "potato": {
        "ph_range": (5.0, 6.0),
        "kc": {"nursery": 0.5, "vegetative": 0.8, "flowering": 1.05, "fruiting": 1.0, "maturity": 0.85},
        "temp_range_c": (15, 20),
        "npk_per_m2": {"vegetative": (1.0, 0.6, 1.0)},
    },
    "maize": {
        "ph_range": (5.8, 7.0),
        "kc": {"nursery": 0.4, "vegetative": 0.85, "flowering": 1.2, "fruiting": 1.1, "maturity": 0.8},
        "temp_range_c": (18, 30),
        "npk_per_m2": {"vegetative": (1.2, 0.5, 0.5)},
    },
    "wheat": {
        "ph_range": (6.0, 7.5),
        "kc": {"nursery": 0.4, "vegetative": 0.8, "flowering": 1.05, "fruiting": 1.0, "maturity": 0.8},
        "temp_range_c": (12, 25),
        "npk_per_m2": {"vegetative": (0.8, 0.4, 0.5)},
    },
    "rice": {
        "ph_range": (5.5, 7.0),
        "kc": {"nursery": 1.0, "vegetative": 1.05, "flowering": 1.2, "fruiting": 1.1, "maturity": 0.9},
        "temp_range_c": (20, 30),
        "npk_per_m2": {"vegetative": (1.0, 0.6, 0.6)},
    },
}


async def _fetch_weather(lat: float, lon: float) -> Dict[str, Any]:
    url = (
        "https://api.open-meteo.com/v1/forecast?latitude="
        f"{lat}&longitude={lon}&hourly=temperature_2m,precipitation,et0_fao_evapotranspiration&forecast_days=3&timezone=auto"
    )
    async with httpx.AsyncClient(timeout=15.0) as client:
        r = await client.get(url)
        if r.status_code != 200:
            raise HTTPException(status_code=502, detail="Weather service unavailable")
        return r.json()


def _avg(values):
    return float(sum(values) / max(len(values), 1))


def _compute_irrigation(ad: AdviceRequest, weather: Dict[str, Any]) -> Dict[str, Any]:
    crop = ad.crop.lower()
    info = _CROP_INFO.get(crop, _CROP_INFO["tomato"])  # default to tomato profile
    kc_map = info["kc"]
    kc = kc_map.get(ad.growth_stage.lower(), _avg(list(kc_map.values())))

    hourly = weather.get("hourly", {})
    et0 = hourly.get("et0_fao_evapotranspiration", [0])
    precip = hourly.get("precipitation", [0])

    et0_daily_mm = _avg(et0) * 24.0  # open-meteo hourly mm/hour
    precip_daily_mm = _avg(precip) * 24.0

    crop_et_mm = max(et0_daily_mm * kc - precip_daily_mm * 0.7, 0.0)
    liters_per_m2 = crop_et_mm  # 1 mm = 1 L/m2
    total_liters = liters_per_m2 * ad.area_m2

    freq = "daily" if liters_per_m2 > 3 else ("every 2 days" if liters_per_m2 > 1 else "every 3 days")

    return {
        "kc": kc,
        "et0_mm_day": round(et0_daily_mm, 2),
        "precip_mm_day": round(precip_daily_mm, 2),
        "recommended_liters_per_m2": round(liters_per_m2, 2),
        "recommended_total_liters": round(total_liters, 2),
        "frequency": freq,
        "note": "Adjust for soil moisture; reduce by 30% on cool/cloudy days and increase by 20% during heat waves.",
    }


def _compute_planting(ad: AdviceRequest, weather: Dict[str, Any]) -> Dict[str, Any]:
    crop = ad.crop.lower()
    info = _CROP_INFO.get(crop, _CROP_INFO["tomato"])  # default
    tmin, tmax = info["temp_range_c"]

    temps = weather.get("hourly", {}).get("temperature_2m", [tmin])
    avg_temp = _avg(temps)

    within_window = tmin <= avg_temp <= tmax
    msg = (
        "Favorable planting window based on 3-day average temperature."
        if within_window
        else f"Suboptimal temps (avg {avg_temp:.1f}°C); target {tmin}-{tmax}°C. Consider transplants or delay."
    )
    return {
        "average_temp_c": round(avg_temp, 1),
        "target_range_c": [tmin, tmax],
        "window": "good" if within_window else "poor",
        "message": msg,
    }


def _compute_soil(ad: AdviceRequest) -> Dict[str, Any]:
    crop = ad.crop.lower()
    info = _CROP_INFO.get(crop, _CROP_INFO["tomato"])  # default
    ph_low, ph_high = info["ph_range"]

    soil_recs = {}
    if ad.soil_ph is not None:
        if ad.soil_ph < ph_low:
            soil_recs["ph"] = f"Raise pH towards {ph_low}-{ph_high}. Apply agricultural lime; re-test in 2-3 weeks."
        elif ad.soil_ph > ph_high:
            soil_recs["ph"] = f"Lower pH towards {ph_low}-{ph_high}. Add elemental sulfur or acidifying fertilizers."
        else:
            soil_recs["ph"] = "pH within target range. Maintain with organic matter."
    else:
        soil_recs["ph"] = "Provide soil pH for tailored recommendations."

    if ad.growth_stage.lower() in ("vegetative",):
        npk = _CROP_INFO[crop]["npk_per_m2"]["vegetative"]
        soil_recs["fertilization_npk_kg_per_100m2"] = [round(x * 0.1, 2) for x in npk]
        soil_recs["note"] = "Split applications; avoid over-fertilization. Base final rates on soil test."

    if ad.soil_moisture_pct is not None:
        if ad.soil_moisture_pct < 15:
            soil_recs["moisture"] = "Soil is dry; increase irrigation frequency and mulch to conserve moisture."
        elif ad.soil_moisture_pct > 35:
            soil_recs["moisture"] = "Soil is wet; improve drainage and reduce irrigation to prevent root diseases."
        else:
            soil_recs["moisture"] = "Soil moisture is moderate; maintain current irrigation."

    if ad.soil_type:
        st = ad.soil_type.lower()
        if st in ("sand", "sandy"):
            soil_recs["soil_type"] = "Sandy soils drain fast; use smaller, more frequent irrigations and add organic matter."
        elif st in ("clay",):
            soil_recs["soil_type"] = "Clay soils hold water; avoid waterlogging and improve structure with compost."
        elif st in ("loam",):
            soil_recs["soil_type"] = "Loam is ideal; maintain structure with cover crops and mulches."

    return soil_recs


@router.post("/", response_model=AdviceResponse)
async def get_advice(req: AdviceRequest) -> AdviceResponse:
    lat = req.latitude if req.latitude is not None else 0.0
    lon = req.longitude if req.longitude is not None else 0.0

    weather = await _fetch_weather(lat, lon)

    irrigation = _compute_irrigation(req, weather)
    planting = _compute_planting(req, weather)
    soil = _compute_soil(req)

    return AdviceResponse(
        irrigation=irrigation,
        planting=planting,
        soil=soil,
        notes="Weather from Open-Meteo; consider local microclimate."
    )