from fastapi import FastAPI
from app.api.routes import router

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Milk Quality API Running"}

app.include_router(router)
