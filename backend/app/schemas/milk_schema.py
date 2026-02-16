from pydantic import BaseModel

class MilkInput(BaseModel):
    ph: float
    temperature: float
    weight: float

class MilkResponse(BaseModel):
    quality_score: float
    status: str
    price_per_liter: float
    total_amount: float
