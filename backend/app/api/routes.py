from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.milk_schema import MilkInput, MilkResponse
from app.services.quality_score import calculate_quality
from app.services.pricing import calculate_price
from app.db.database import SessionLocal
from app.db.crud import create_milk_record
from app.db.crud import get_all_records, get_records_by_vendor


router = APIRouter()

# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/analyze", response_model=MilkResponse)
def analyze_milk(data: MilkInput, db: Session = Depends(get_db)):

    # 1️⃣ Calculate Quality Score
    score = calculate_quality(data.ph, data.temperature)

    # 2️⃣ Calculate Pricing
    status, price, total = calculate_price(score, data.weight)

    # 3️⃣ Prepare Data for Database
    db_data = {
        "vendor_id": 1,  # Later you can make dynamic
        "ph": data.ph,
        "temperature": data.temperature,
        "weight": data.weight,
        "risk_level": status,   # using status as risk level
        "probability": float(score) / 100,  # temporary logic
        "spoilage_hours": 6 if status == "Accept" else 3,
        "price_per_liter": price,
        "total_amount": total
    }

    # 4️⃣ Save to Database
    create_milk_record(db, db_data)

    # 5️⃣ Return Response
    return MilkResponse(
        quality_score=score,
        status=status,
        price_per_liter=price,
        total_amount=total
    )
@router.get("/records")
def fetch_all_records(db: Session = Depends(get_db)):
    records = get_all_records(db)
    return records


@router.get("/records/{vendor_id}")
def fetch_vendor_records(vendor_id: int, db: Session = Depends(get_db)):
    records = get_records_by_vendor(db, vendor_id)
    return records
