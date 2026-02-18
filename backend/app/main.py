from fastapi import FastAPI
from app.api.routes import router
from app.db.init_db import init_db
from app.api.routes import router as api_router
from app.api.agent_routes import router as agent_router

from app.auth.auth_routes import router as auth_router
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
app.include_router(api_router)
app.include_router(auth_router)

app.include_router(agent_router)