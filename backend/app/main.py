from fastapi import FastAPI
from app.api.routes import router
from app.db.init_db import init_db

# Create FastAPI app
app = FastAPI(title="AI Smart Milk Monitoring System")

# Initialize database (creates tables if not exist)
init_db()

# Root test endpoint
@app.get("/")
def root():
    return {"message": "Milk Quality API Running"}

# Include API routes
app.include_router(router)
