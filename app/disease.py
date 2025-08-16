from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List, Tuple
from PIL import Image
import colorsys

router = APIRouter()


class DiseasePrediction(BaseModel):
    disease_name: str
    confidence: float
    features: Dict[str, float]
    recommendations: str


def _read_image(image_file: UploadFile) -> Image.Image:
    try:
        image = Image.open(image_file.file).convert("RGB")
        image = image.resize((256, 256))
        return image
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Invalid image: {exc}")


def _rgb_to_hsv_pixel(r: int, g: int, b: int) -> Tuple[float, float, float]:
    # colorsys returns h in [0,1), s,v in [0,1]
    h, s, v = colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)
    return h * 360.0, s, v


def _compute_leaf_mask(s: float, v: float) -> bool:
    return (s > 0.1) and (v > 0.1)


def _count_components(mask: List[List[bool]], min_area: int = 10) -> int:
    h = len(mask)
    w = len(mask[0]) if h else 0
    visited = [[False] * w for _ in range(h)]
    count = 0

    for y in range(h):
        for x in range(w):
            if mask[y][x] and not visited[y][x]:
                stack = [(y, x)]
                visited[y][x] = True
                area = 0
                while stack:
                    sy, sx = stack.pop()
                    area += 1
                    for ny, nx in ((sy - 1, sx), (sy + 1, sx), (sy, sx - 1), (sy, sx + 1)):
                        if 0 <= ny < h and 0 <= nx < w and mask[ny][nx] and not visited[ny][nx]:
                            visited[ny][nx] = True
                            stack.append((ny, nx))
                if area >= min_area:
                    count += 1
    return count


def _extract_features(image: Image.Image) -> Dict[str, float]:
    width, height = image.size
    pixels = image.load()

    total_mask = 0
    green_count = 0
    yellow_count = 0
    brown_count = 0
    white_count = 0

    dark_mask: List[List[bool]] = [[False] * width for _ in range(height)]

    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]
            h, s, v = _rgb_to_hsv_pixel(r, g, b)
            is_leaf = _compute_leaf_mask(s, v)
            if not is_leaf:
                continue
            total_mask += 1

            if 60 <= h <= 170 and s > 0.2 and v > 0.2:
                green_count += 1
            if 25 <= h < 60 and s > 0.2 and v > 0.2:
                yellow_count += 1
            if ((10 <= h < 25) or (v < 0.35 and r > g > b)):
                brown_count += 1
            if (v > 0.9 and s < 0.2):
                white_count += 1
            if v < 0.25:
                dark_mask[y][x] = True

    total = float(max(total_mask, 1))

    dark_spot_ratio = sum(1 for row in dark_mask for v in row if v) / total
    dark_spot_count = _count_components(dark_mask, min_area=10) / 100.0

    return {
        "green_ratio": green_count / total,
        "yellow_ratio": yellow_count / total,
        "brown_ratio": brown_count / total,
        "white_ratio": white_count / total,
        "dark_spot_ratio": dark_spot_ratio,
        "dark_spot_count_norm": dark_spot_count,
    }


def _classify(features: Dict[str, float]) -> DiseasePrediction:
    green = features["green_ratio"]
    yellow = features["yellow_ratio"]
    brown = features["brown_ratio"]
    white = features["white_ratio"]
    dark_spot = features["dark_spot_ratio"]
    dark_count = features["dark_spot_count_norm"]

    scores: Dict[str, float] = {}

    scores["Healthy"] = max(0.0, green - (yellow + brown + white + dark_spot))
    scores["Powdery Mildew (Fungal)"] = max(0.0, white * 1.5 + (green * 0.2) - (brown + yellow + dark_spot) * 0.3)
    scores["Leaf Blight / Rust (Fungal)"] = max(0.0, brown * 1.2 + dark_count * 0.5 + (yellow * 0.2) - white * 0.2)
    scores["Bacterial Spot"] = max(0.0, dark_spot * 1.4 + dark_count * 0.8 - white * 0.2)
    scores["Nutrient Deficiency (Nitrogen)"] = max(0.0, yellow * 1.3 - brown * 0.2 - white * 0.2)

    label_name = max(scores, key=scores.get)
    raw_score = scores[label_name]
    confidence = float(min(max(raw_score / 1.5, 0.05), 0.98))

    recommendations_map = {
        "Healthy": "Plant appears healthy. Maintain regular scouting, balanced fertilization, and proper irrigation.",
        "Powdery Mildew (Fungal)": "Remove heavily infected leaves. Improve airflow. Apply sulfur or potassium bicarbonate. Consider fungicides with FRAC codes 3 or 11, rotating modes.",
        "Leaf Blight / Rust (Fungal)": "Prune affected tissue, avoid overhead irrigation. Apply protectant fungicides (chlorothalonil, mancozeb) and rotate systemic options per FRAC.",
        "Bacterial Spot": "Avoid working plants when wet. Copper-based bactericides can help suppress; rotate and monitor phytotoxicity. Remove crop residues.",
        "Nutrient Deficiency (Nitrogen)": "Side-dress Nitrogen (e.g., urea) in split applications. Mulch and manage irrigation to reduce leaching. Verify with soil test.",
    }

    return DiseasePrediction(
        disease_name=label_name,
        confidence=confidence,
        features=features,
        recommendations=recommendations_map.get(label_name, ""),
    )


@router.post("/predict", response_model=DiseasePrediction)
async def predict_disease(file: UploadFile = File(...)) -> Any:
    img = _read_image(file)
    features = _extract_features(img)
    prediction = _classify(features)
    return prediction