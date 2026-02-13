from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.schemas.order import OrderCreate, OrderUpdate
from app.services.customer_service import get_or_create_customer
from app.services.order_service import *
from app.services.sms_service import send_sms

router = APIRouter(prefix="/orders", tags=["Orders"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def place_order(data: OrderCreate, db: Session = Depends(get_db)):
    customer = get_or_create_customer(
        db,
        name=data.name,
        phone=data.phone,
        address=data.address
    )

    order = create_order(db, customer.id, data.items)

    send_sms(customer.phone, f"Order #{order.id} confirmed!")

    return order


@router.put("/{order_id}")
def update(order_id: int, data: OrderUpdate, db: Session = Depends(get_db)):
    order = update_order(db, order_id, data.items)
    if not order:
        raise HTTPException(404, "Order not found")
    return order


@router.post("/{order_id}/cancel")
def cancel(order_id: int, db: Session = Depends(get_db)):
    result = cancel_order(db, order_id)

    if result == "expired":
        raise HTTPException(400, "Cancel window expired")

    if not result:
        raise HTTPException(404, "Order not found")

    return result


@router.get("/{order_id}/status")
def status(order_id: int, db: Session = Depends(get_db)):
    order = get_order_status(db, order_id)
    if not order:
        raise HTTPException(404, "Order not found")
    return {"order_id": order.id, "status": order.status}