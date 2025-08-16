import os
import base64
from typing import Optional, Dict, Any, List

import streamlit as st
from PIL import Image

from ai.vision import detect_disease_from_image
from ai.advice import generate_farming_advice
from utils.weather import get_weather_for_location
from utils.location import geocode_location_to_coords, normalize_region_name
from utils.pricing import load_price_dataset, suggest_fair_price, load_buyer_directory, find_buyers


st.set_page_config(page_title="AI Farmer Assistant", page_icon="🌾", layout="wide")

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")


def _section_header(title: str, subtitle: Optional[str] = None):
    st.markdown(f"### {title}")
    if subtitle:
        st.caption(subtitle)


@st.cache_data(show_spinner=False)
def _load_datasets():
    prices = load_price_dataset()
    buyers = load_buyer_directory()
    return prices, buyers


prices_dataset, buyers_dataset = _load_datasets()

st.sidebar.title("AI Farmer Assistant")
st.sidebar.write("Identify crop diseases, get real-time advice, and find fair prices & buyers.")

section = st.sidebar.radio(
    "Go to",
    ["Disease Diagnosis", "Farming Advice", "Prices & Buyers"],
)


# Disease Diagnosis
if section == "Disease Diagnosis":
    _section_header("Identify crop diseases from a photo", "Upload a leaf/crop image for diagnosis")

    col_left, col_right = st.columns([1, 1])

    with col_left:
        crop = st.selectbox(
            "Crop",
            [
                "Tomato",
                "Potato",
                "Wheat",
                "Rice",
                "Maize",
                "Cotton",
                "Soybean",
                "Cassava",
                "Banana",
                "Grape",
            ],
            index=0,
        )
        image_file = st.file_uploader(
            "Upload crop/leaf photo (JPG/PNG)", type=["jpg", "jpeg", "png"], accept_multiple_files=False
        )
        use_llm = st.toggle(
            "Use AI model (requires OPENAI_API_KEY)", value=bool(OPENAI_API_KEY),
            help="Enable if you want LLM-based image diagnosis. Falls back to local heuristics if disabled or no key."
        )
        analyze_btn = st.button("Analyze Photo", type="primary", disabled=image_file is None)

    with col_right:
        if image_file:
            img = Image.open(image_file).convert("RGB")
            st.image(img, caption="Uploaded image", use_column_width=True)

    if analyze_btn and image_file is not None:
        with st.spinner("Analyzing image..."):
            image_bytes = image_file.getvalue()
            result = detect_disease_from_image(
                image_bytes=image_bytes,
                crop=crop,
                openai_api_key=OPENAI_API_KEY if use_llm else None,
            )

        if result.get("error"):
            st.error(result["error"]) 
        else:
            st.success("Diagnosis complete")
            st.write("**Predicted disease:**", result.get("disease_name", "Unknown"))
            st.write("**Crop:**", result.get("crop", crop))
            conf = result.get("confidence")
            if conf is not None:
                st.write("**Confidence:**", f"{conf:.0%}")
            st.write("**Description:**")
            st.write(result.get("description") or "—")

            actions: List[str] = result.get("recommended_actions") or []
            if actions:
                st.write("**Recommended actions:**")
                for idx, act in enumerate(actions, start=1):
                    st.write(f"{idx}. {act}")

            st.caption("Note: This tool provides decision support and should complement expert agronomist advice.")


# Farming Advice
elif section == "Farming Advice":
    _section_header("Real-time farming advice", "Weather-aware guidance for planting, soil and irrigation")

    with st.form("advice_form"):
        col1, col2, col3 = st.columns(3)
        with col1:
            location_query = st.text_input("Location (city, village, or coordinates)", placeholder="e.g., Eldoret, Kenya")
            crop = st.selectbox(
                "Crop",
                ["Tomato", "Potato", "Wheat", "Rice", "Maize", "Cotton", "Soybean", "Cassava", "Banana", "Grape"],
            )
        with col2:
            soil_ph = st.slider("Soil pH", min_value=3.5, max_value=9.5, value=6.5, step=0.1)
            irrigation_method = st.selectbox("Irrigation method", ["Rainfed", "Drip", "Sprinkler", "Flood"]) 
        with col3:
            soil_moisture_pct = st.slider("Soil moisture (%)", min_value=0, max_value=100, value=35)
            crop_stage = st.selectbox("Crop stage", ["Pre-planting", "Vegetative", "Flowering", "Fruiting/Grain filling", "Maturity"]) 

        submit = st.form_submit_button("Get Advice", type="primary")

    if submit:
        if not location_query:
            st.warning("Please provide a location to tailor advice with local weather.")
        else:
            with st.spinner("Fetching weather and generating advice..."):
                coords = geocode_location_to_coords(location_query)
                weather = None
                if coords:
                    weather = get_weather_for_location(latitude=coords["latitude"], longitude=coords["longitude"]) 
                advice = generate_farming_advice(
                    crop=crop,
                    soil_ph=soil_ph,
                    irrigation_method=irrigation_method,
                    soil_moisture_pct=soil_moisture_pct,
                    crop_stage=crop_stage,
                    location_query=location_query,
                    weather=weather,
                    openai_api_key=OPENAI_API_KEY,
                )

            if advice.get("error"):
                st.error(advice["error"]) 
            else:
                st.subheader("Guidance")

                bullets = advice.get("key_recommendations") or []
                for idx, rec in enumerate(bullets, start=1):
                    st.write(f"{idx}. {rec}")

                if advice.get("irrigation_schedule"):
                    st.write("**Irrigation schedule:**")
                    st.write(advice["irrigation_schedule"]) 

                if weather:
                    st.caption(
                        f"Weather snapshot for {location_query} — Temp: {weather['current'].get('temperature_c')}°C, "
                        f"Wind: {weather['current'].get('windspeed_kmh')} km/h, "
                        f"Precip (next 24h): {weather['forecast'].get('precip_next_24h_mm')} mm"
                    )


# Prices & Buyers
elif section == "Prices & Buyers":
    _section_header("Suggest fair prices & connect to buyers", "Market guidance and nearby buyer leads")

    col_a, col_b = st.columns([1, 1])
    with col_a:
        crop = st.selectbox("Crop", sorted(set(p["crop"] for p in prices_dataset)))
        region_input = st.text_input("Your region (country or state/province)", placeholder="e.g., Kenya or Maharashtra, India")
        quantity = st.number_input("Quantity available (tonnes)", min_value=0.0, value=1.0, step=0.1)
        calc_btn = st.button("Suggest Price & Buyers", type="primary")

    if calc_btn:
        if not region_input:
            st.warning("Please input a region to localize pricing and buyers.")
        else:
            with st.spinner("Computing fair price and finding buyers..."):
                norm_region = normalize_region_name(region_input)
                suggestion = suggest_fair_price(crop=crop, region=norm_region, quantity_tonnes=quantity)
                buyers = find_buyers(crop=crop, region=norm_region)

            st.subheader("Fair Price Suggestion")
            st.write(f"**Estimated fair price:** {suggestion['currency']} {suggestion['fair_price_per_tonne']:.2f} per tonne")
            st.write(f"**Negotiation range:** {suggestion['currency']} {suggestion['low_per_tonne']:.2f} - {suggestion['high_per_tonne']:.2f} per tonne")
            st.caption("Based on local/national reference prices, adjusted for seasonality and demand where available.")

            if buyers:
                st.subheader("Potential Buyers")
                for b in buyers:
                    st.write(
                        f"- {b['name']} — {b.get('type','Buyer')} in {b.get('region','')}. "
                        f"Contact: {b.get('contact','N/A')}. Accepts: {', '.join(b.get('crops', []))}"
                    )
            else:
                st.info("No local buyers found in the sample directory. Consider contacting nearby cooperatives or online marketplaces.")

st.sidebar.caption("Tip: Set OPENAI_API_KEY in environment for best results.")