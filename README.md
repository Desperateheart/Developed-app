# AI Farmer Assistant

A prototype FastAPI service that helps farmers by:

1. Identifying crop diseases from photos
2. Providing real-time farming advice on topics like planting, soil, and irrigation
3. Suggesting fair prices and connecting farmers with potential buyers

## Getting Started

### Requirements

* Python 3.9+
* See `requirements.txt` for Python dependencies

### Installation

```bash
# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Running the API server

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Navigate to `http://localhost:8000/docs` for the interactive Swagger UI.

## Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/predict-disease` | Upload an image (`file`) and receive a disease prediction and confidence. |
| GET | `/advice?topic=soil` | Get farming advice for a specific topic (planting, soil, irrigation, etc.). |
| GET | `/price?crop=maize&quantity=500` | Receive a price suggestion per kg, total price, and potential buyers. |

## Limitations & TODO

* The disease classifier currently uses a placeholder model; integrate a fine-tuned crop-disease model.
* Price suggestions are heuristic; connect to real market APIs.
* Buyer database is static.
* Consider adding user authentication and history tracking.