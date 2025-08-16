from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
from sqlmodel import SQLModel, Field, create_engine, Session, select
import os

router = APIRouter()

_DB_PATH = os.path.join(os.getcwd(), "data")
_DB_FILE = os.path.join(_DB_PATH, "farmer_assistant.sqlite")
_engine = None


class Listing(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)
    seller_name: str
    crop: str
    quantity_kg: float
    price_per_kg: float
    region: str
    contact_info: str
    description: Optional[str] = None


class Offer(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)
    listing_id: int = Field(index=True)
    buyer_name: str
    offered_price_per_kg: float
    quantity_kg: float
    contact_info: str
    message: Optional[str] = None


class PriceHistory(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    date: datetime = Field(default_factory=datetime.utcnow, index=True)
    crop: str = Field(index=True)
    region: str = Field(index=True)
    price_per_kg: float


class ListingRequest(BaseModel):
    seller_name: str
    crop: str
    quantity_kg: float
    price_per_kg: float
    region: str
    contact_info: str
    description: Optional[str] = None


class OfferRequest(BaseModel):
    listing_id: int
    buyer_name: str
    offered_price_per_kg: float
    quantity_kg: float
    contact_info: str
    message: Optional[str] = None


_FAIR_PRICE_BASELINE = {
    "tomato": 0.8,
    "potato": 0.5,
    "maize": 0.35,
    "wheat": 0.4,
    "rice": 0.6,
}


def _get_engine():
    global _engine
    if _engine is None:
        os.makedirs(_DB_PATH, exist_ok=True)
        _engine = create_engine(f"sqlite:///{_DB_FILE}", echo=False)
    return _engine


def init_db_and_seed() -> None:
    engine = _get_engine()
    SQLModel.metadata.create_all(engine)
    # Seed example data if empty
    with Session(engine) as session:
        has_listing = session.exec(select(Listing).limit(1)).first() is not None
        if not has_listing:
            now = datetime.utcnow()
            samples = [
                Listing(seller_name="Asha", crop="tomato", quantity_kg=150, price_per_kg=0.9, region="Nairobi", contact_info="+2547000001"),
                Listing(seller_name="Carlos", crop="potato", quantity_kg=400, price_per_kg=0.52, region="Lima", contact_info="+510100200"),
                Listing(seller_name="Mei", crop="rice", quantity_kg=800, price_per_kg=0.62, region="Guangxi", contact_info="+861300000"),
                Listing(seller_name="Ravi", crop="wheat", quantity_kg=600, price_per_kg=0.42, region="Punjab", contact_info="+911100200"),
            ]
            for s in samples:
                session.add(s)

            # Seed price history last 30 days
            crops = list(_FAIR_PRICE_BASELINE.keys())
            regions = ["Nairobi", "Lima", "Guangxi", "Punjab"]
            for d in range(30):
                for crop in crops:
                    for region in regions:
                        base = _FAIR_PRICE_BASELINE[crop]
                        # random-ish small fluctuation without randomness for determinism
                        delta = ((d % 7) - 3) * 0.01
                        ph = PriceHistory(date=now - timedelta(days=d), crop=crop, region=region, price_per_kg=round(base + delta, 2))
                        session.add(ph)
            session.commit()


@router.get("/listings", response_model=List[Dict[str, Any]])
def list_listings(crop: Optional[str] = None, region: Optional[str] = None) -> List[Dict[str, Any]]:
    engine = _get_engine()
    with Session(engine) as session:
        stmt = select(Listing)
        if crop:
            stmt = stmt.where(Listing.crop == crop)
        if region:
            stmt = stmt.where(Listing.region == region)
        results = session.exec(stmt.order_by(Listing.created_at.desc()).limit(200)).all()
        return [l.model_dump() for l in results]


@router.post("/listings", response_model=Dict[str, Any])
def create_listing(req: ListingRequest) -> Dict[str, Any]:
    engine = _get_engine()
    listing = Listing(**req.model_dump())
    with Session(engine) as session:
        session.add(listing)
        session.commit()
        session.refresh(listing)
    return listing.model_dump()


@router.post("/offers", response_model=Dict[str, Any])
def create_offer(req: OfferRequest) -> Dict[str, Any]:
    engine = _get_engine()
    # validate listing exists
    with Session(engine) as session:
        lst = session.exec(select(Listing).where(Listing.id == req.listing_id)).first()
        if lst is None:
            raise HTTPException(status_code=404, detail="Listing not found")
        offer = Offer(**req.model_dump())
        session.add(offer)
        session.commit()
        session.refresh(offer)
        return offer.model_dump()


@router.get("/offers", response_model=List[Dict[str, Any]])
def get_offers(listing_id: int = Query(...)) -> List[Dict[str, Any]]:
    engine = _get_engine()
    with Session(engine) as session:
        offers = session.exec(select(Offer).where(Offer.listing_id == listing_id).order_by(Offer.created_at.desc())).all()
        return [o.model_dump() for o in offers]


@router.get("/fair_price", response_model=Dict[str, Any])
def fair_price(crop: str, region: Optional[str] = None) -> Dict[str, Any]:
    engine = _get_engine()
    now = datetime.utcnow()
    since = now - timedelta(days=30)
    with Session(engine) as session:
        stmt = select(PriceHistory).where(PriceHistory.crop == crop)
        if region:
            stmt = stmt.where(PriceHistory.region == region)
        stmt = stmt.where(PriceHistory.date >= since)
        prices = [ph.price_per_kg for ph in session.exec(stmt).all()]
        if prices:
            prices_sorted = sorted(prices)
            n = len(prices_sorted)
            median = prices_sorted[n // 2] if n % 2 == 1 else (prices_sorted[n // 2 - 1] + prices_sorted[n // 2]) / 2
            return {
                "crop": crop,
                "region": region,
                "median_price_per_kg": round(float(median), 2),
                "data_points": n,
                "source": "local_market_history",
            }
        # fallback
        baseline = _FAIR_PRICE_BASELINE.get(crop.lower())
        if baseline is None:
            raise HTTPException(status_code=404, detail="No price data for crop")
        return {
            "crop": crop,
            "region": region,
            "median_price_per_kg": baseline,
            "data_points": 0,
            "source": "baseline",
        }