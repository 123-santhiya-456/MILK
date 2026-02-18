from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from app.db.database import SessionLocal
from app.models.admin_model import Admin
from app.auth.auth_utils import verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["Authentication"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    admin = db.query(Admin).filter(
        Admin.username == form_data.username
    ).first()

    if not admin:
        raise HTTPException(status_code=400, detail="Invalid username")

    if not verify_password(form_data.password, admin.password):
        raise HTTPException(status_code=400, detail="Invalid password")

    access_token = create_access_token(data={"sub": admin.username})

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
