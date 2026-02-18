import os
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from dotenv import load_dotenv
from openai import OpenAI

from app.db.database import SessionLocal
from app.models.milk_model import MilkRecord
from app.models.vendor_model import Vendor
from app.schemas.agent_schema import AgentRequest, AgentResponse


GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise RuntimeError("GROQ_API_KEY not found in .env file")

# Groq client
client = OpenAI(
    api_key="GROQ_API_KEY",
    base_url="https://api.groq.com/openai/v1"
)

router = APIRouter(prefix="/agent", tags=["AI Agent"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/ask", response_model=AgentResponse)
def ask_agent(data: AgentRequest, db: Session = Depends(get_db)):

    # Collect DB data
    total_revenue = db.query(func.sum(MilkRecord.total_amount)).scalar() or 0
    total_milk = db.query(func.sum(MilkRecord.weight)).scalar() or 0

    vendor_data = db.query(
        Vendor.name,
        func.sum(MilkRecord.total_amount)
    ).join(MilkRecord).group_by(Vendor.name).all()

    context = f"""
    Total Revenue: {total_revenue}
    Total Milk Collected: {total_milk}
    Vendor Revenue Data: {vendor_data}
    """

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",  # ✅ updated model
            messages=[
                {"role": "system", "content": "You are a dairy analytics assistant."},
                {
                    "role": "user",
                    "content": f"Here is the data:\n{context}\n\nQuestion: {data.question}"
                }
            ],
            temperature=0.3
        )

        return AgentResponse(
            answer=response.choices[0].message.content
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
