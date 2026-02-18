from pydantic import BaseModel

class MilkInput(BaseModel):
    vendor_id: int   # 🔥 Added
    ph: float
    temperature: float
    weight: float


class MilkResponse(BaseModel):
    vendor_id: int
    quality_score: float
    status: str
    price_per_liter: float
    total_amount: float
