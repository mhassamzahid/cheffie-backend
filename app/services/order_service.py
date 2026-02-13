from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models.order import Order

CANCEL_WINDOW_MINUTES = 15


def create_order(db: Session, customer_id: int, items: list):
    order = Order(customer_id=customer_id, items=items)
    db.add(order)
    db.commit()
    db.refresh(order)
    return order


def update_order(db: Session, order_id: int, items: list):
    order = db.get(Order, order_id)
    if not order:
        return None

    order.items = items
    db.commit()
    return order


def cancel_order(db: Session, order_id: int):
    order = db.get(Order, order_id)
    if not order:
        return None

    created_time = order.created_at.replace(tzinfo=None)
    if datetime.utcnow() - created_time > timedelta(minutes=CANCEL_WINDOW_MINUTES):
        return "expired"

    order.status = "cancelled"
    db.commit()
    return order


def get_order_status(db: Session, order_id: int):
    return db.get(Order, order_id)