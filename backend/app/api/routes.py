from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, desc

from app.db.database import SessionLocal
from app.db.crud import create_milk_record, get_all_records, get_records_by_vendor

from app.schemas.milk_schema import MilkInput, MilkResponse
from app.services.quality_score import calculate_quality
from app.services.pricing import calculate_price

from app.models.vendor_model import Vendor
from app.models.milk_model import MilkRecord

from app.auth.dependencies import get_current_admin   # 🔒 JWT Protection

router = APIRouter()


# =========================
# Database Dependency
# =========================
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# =========================
# Milk Analysis
# =========================
@router.post("/analyze", response_model=MilkResponse)
def analyze_milk(
    data: MilkInput,
    db: Session = Depends(get_db),
    current_admin: str = Depends(get_current_admin)  # 🔒 Protected
):

    # 0️⃣ Check Vendor Exists
    vendor = db.query(Vendor).filter(Vendor.id == data.vendor_id).first()
    if not vendor:
        raise HTTPException(status_code=404, detail="Vendor not found")

    # 1️⃣ Calculate Quality Score
    score = calculate_quality(data.ph, data.temperature,data.weight)
    

    # 2️⃣ Calculate Pricing
    status, price, total = calculate_price(score, data.weight)

    # 3️⃣ Prepare Data
    db_data = {
        "vendor_id": data.vendor_id,
        "ph": data.ph,
        "temperature": data.temperature,
        "weight": data.weight,
        "risk_level": status,
        "probability": float(score) / 100,
        "spoilage_hours": 6 if status == "Accept" else 3,
        "price_per_liter": price,
        "total_amount": total
    }

    # 4️⃣ Save Record
    create_milk_record(db, db_data)

    # 5️⃣ Return Response
    return MilkResponse(
        vendor_id=data.vendor_id,
        quality_score=score,
        status=status,
        price_per_liter=price,
        total_amount=total
    )


# =========================
# Records
# =========================
@router.get("/records")
def fetch_all_records(
    db: Session = Depends(get_db),
    current_admin: str = Depends(get_current_admin)  # 🔒 Protected
):
    return get_all_records(db)


@router.get("/records/{vendor_id}")
def fetch_vendor_records(
    vendor_id: int,
    db: Session = Depends(get_db),
    current_admin: str = Depends(get_current_admin)  # 🔒 Protected
):
    return get_records_by_vendor(db, vendor_id)


# =========================
# Dashboard Summary
# =========================
@router.get("/dashboard/summary")
def dashboard_summary(
    db: Session = Depends(get_db),
    current_admin: str = Depends(get_current_admin)  # 🔒 Protected
):

    total_milk = db.query(func.sum(MilkRecord.weight)).scalar() or 0
    total_revenue = db.query(func.sum(MilkRecord.total_amount)).scalar() or 0
    avg_quality = db.query(func.avg(MilkRecord.probability)).scalar() or 0

    total_records = db.query(MilkRecord).count()
    spoiled_count = db.query(MilkRecord).filter(
        MilkRecord.risk_level == "Reject"
    ).count()

    spoilage_percentage = (
        (spoiled_count / total_records) * 100
        if total_records > 0 else 0
    )

    return {
        "total_milk_collected": total_milk,
        "total_revenue": total_revenue,
        "average_quality": round(avg_quality * 100, 2),
        "spoilage_percentage": round(spoilage_percentage, 2)
    }


# =========================
# Vendor Dashboard
# =========================
@router.get("/dashboard/vendor/{vendor_id}")
def vendor_dashboard(
    vendor_id: int,
    db: Session = Depends(get_db),
    current_admin: str = Depends(get_current_admin)  # 🔒 Protected
):

    vendor = db.query(Vendor).filter(Vendor.id == vendor_id).first()
    if not vendor:
        raise HTTPException(status_code=404, detail="Vendor not found")

    total_milk = db.query(func.sum(MilkRecord.weight)).filter(
        MilkRecord.vendor_id == vendor_id
    ).scalar() or 0

    total_revenue = db.query(func.sum(MilkRecord.total_amount)).filter(
        MilkRecord.vendor_id == vendor_id
    ).scalar() or 0

    avg_quality = db.query(func.avg(MilkRecord.probability)).filter(
        MilkRecord.vendor_id == vendor_id
    ).scalar() or 0

    total_records = db.query(MilkRecord).filter(
        MilkRecord.vendor_id == vendor_id
    ).count()

    spoiled_count = db.query(MilkRecord).filter(
        MilkRecord.vendor_id == vendor_id,
        MilkRecord.risk_level == "Reject"
    ).count()

    spoilage_percentage = (
        (spoiled_count / total_records) * 100
        if total_records > 0 else 0
    )

    return {
        "vendor_id": vendor.id,
        "vendor_name": vendor.name,
        "total_milk": total_milk,
        "total_revenue": total_revenue,
        "average_quality": round(avg_quality * 100, 2),
        "total_transactions": total_records,
        "spoilage_percentage": round(spoilage_percentage, 2)
    }


# =========================
# Vendor Ranking
# =========================
@router.get("/dashboard/vendor-ranking")
def vendor_ranking(
    db: Session = Depends(get_db),
    current_admin: str = Depends(get_current_admin)  # 🔒 Protected
):

    results = (
        db.query(
            Vendor.id,
            Vendor.name,
            func.sum(MilkRecord.weight).label("total_milk"),
            func.sum(MilkRecord.total_amount).label("total_revenue")
        )
        .join(MilkRecord, Vendor.id == MilkRecord.vendor_id)
        .group_by(Vendor.id)
        .order_by(desc("total_revenue"))
        .all()
    )

    return [
        {
            "vendor_id": v.id,
            "vendor_name": v.name,
            "total_milk": v.total_milk or 0,
            "total_revenue": v.total_revenue or 0
        }
        for v in results
    ]


# =========================
# Daily Trend
# =========================
@router.get("/dashboard/daily-trend")
def daily_trend(
    db: Session = Depends(get_db),
    current_admin: str = Depends(get_current_admin)  # 🔒 Protected
):

    results = (
        db.query(
            func.date(MilkRecord.timestamp).label("date"),
            func.sum(MilkRecord.weight).label("total_milk"),
            func.sum(MilkRecord.total_amount).label("total_revenue")
        )
        .group_by(func.date(MilkRecord.timestamp))
        .order_by(func.date(MilkRecord.timestamp))
        .all()
    )

    return [
        {
            "date": row.date,
            "total_milk": row.total_milk or 0,
            "total_revenue": row.total_revenue or 0
        }
        for row in results
    ]
