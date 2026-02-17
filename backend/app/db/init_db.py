from app.db.database import engine
from app.db.database import Base
from app.models.milk_model import MilkRecord

def init_db():
    Base.metadata.create_all(bind=engine)
