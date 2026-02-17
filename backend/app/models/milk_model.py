from sqlalchemy import Column, Integer, Float, String, DateTime
from datetime import datetime
from app.db.database import Base

class MilkRecord(Base):
    __tablename__ = "milk_records"

    id = Column(Integer, primary_key=True, index=True)

    vendor_id = Column(Integer)

    ph = Column(Float)
    temperature = Column(Float)
    weight = Column(Float)

    risk_level = Column(String)
    probability = Column(Float)
    spoilage_hours = Column(Integer)

    price_per_liter = Column(Float)
    total_amount = Column(Float)

    timestamp = Column(DateTime, default=datetime.utcnow)
