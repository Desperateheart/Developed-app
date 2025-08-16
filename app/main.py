from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .disease import router as disease_router
from .advice import router as advice_router
from .market import router as market_router, init_db_and_seed

app = FastAPI(title="AI Farmer Assistant", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(disease_router, prefix="/api/disease", tags=["disease"])
app.include_router(advice_router, prefix="/api/advice", tags=["advice"])
app.include_router(market_router, prefix="/api/market", tags=["market"])

# Static UI
app.mount("/ui", StaticFiles(directory="web", html=True), name="ui")


@app.on_event("startup")
async def on_startup() -> None:
    init_db_and_seed()


@app.get("/")
async def root():
    return {"message": "AI Farmer Assistant API running.", "ui": "/ui/"}