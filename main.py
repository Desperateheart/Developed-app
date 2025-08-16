from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from PIL import Image
import io
import torch
import torchvision.transforms as transforms

from modules.disease import DiseaseClassifier
from modules.advice import get_farming_advice
from modules.price import get_price_suggestion

app = FastAPI(title="AI Farmer Assistant",
              description="Identify crop diseases, provide farming advice, and suggest fair prices.",
              version="0.1.0")

# Load classifier once at startup
classifier = DiseaseClassifier()


def read_imagefile(file: UploadFile) -> Image.Image:
    """Read uploaded file to PIL Image"""
    image_bytes = io.BytesIO(file.file.read())
    try:
        img = Image.open(image_bytes).convert("RGB")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid image file: {e}")
    return img


@app.post("/predict-disease")
async def predict_disease(file: UploadFile = File(...)):
    """Predict disease from an uploaded crop image"""
    img = read_imagefile(file)
    prediction, confidence = classifier.predict(img)
    return {"prediction": prediction, "confidence": confidence}


@app.get("/advice")
async def advice(topic: str):
    """Get farming advice for a topic (e.g., planting, soil, irrigation)"""
    advice_text = get_farming_advice(topic)
    if advice_text is None:
        raise HTTPException(status_code=404, detail="No advice available for the specified topic.")
    return {"topic": topic, "advice": advice_text}


@app.get("/price")
async def price(crop: str, quantity: float):
    """Suggest fair price for a crop and connect to buyers (stub). Quantity in kg."""
    suggestion = get_price_suggestion(crop, quantity)
    if suggestion is None:
        raise HTTPException(status_code=404, detail="Price suggestion not available for the specified crop.")
    return suggestion


@app.get("/")
async def root():
    return {"message": "Welcome to AI Farmer Assistant!"}