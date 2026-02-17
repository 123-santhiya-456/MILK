from sqlalchemy.orm import Session
from app.models.milk_model import MilkRecord


def create_milk_record(db: Session, data: dict):
    record = MilkRecord(
        vendor_id=data["vendor_id"],
        ph=data["ph"],
        temperature=data["temperature"],
        weight=data["weight"],
        risk_level=data["risk_level"],
        probability=data["probability"],
        spoilage_hours=data["spoilage_hours"],
        price_per_liter=data["price_per_liter"],
        total_amount=data["total_amount"]
    )

    db.add(record)
    db.commit()
    db.refresh(record)

    return record


def get_all_records(db: Session):
    return db.query(MilkRecord).all()


def get_records_by_vendor(db: Session, vendor_id: int):
    return db.query(MilkRecord).filter(
        MilkRecord.vendor_id == vendor_id
    ).all()
