from fastapi import APIRouter
from app.schemas.milk_schema import MilkInput, MilkResponse
from app.services.quality_score import calculate_quality
from app.services.pricing import calculate_price

router = APIRouter()

@router.post("/analyze", response_model=MilkResponse)
def analyze_milk(data: MilkInput):
    score = calculate_quality(data.ph, data.temperature)
    status, price, total = calculate_price(score, data.weight)

    return MilkResponse(
        quality_score=score,
        status=status,
        price_per_liter=price,
        total_amount=total
    )
