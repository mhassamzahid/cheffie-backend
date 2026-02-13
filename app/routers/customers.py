from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.schemas.customer import CustomerCreate
from app.services.customer_service import get_or_create_customer

router = APIRouter(prefix="/customers", tags=["Customers"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def create_customer(data: CustomerCreate, db: Session = Depends(get_db)):
    return get_or_create_customer(db, data.name, data.phone, data.address)