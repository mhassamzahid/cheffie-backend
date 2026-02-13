from sqlalchemy.orm import Session
from app.models.customer import Customer

def get_or_create_customer(db: Session, name: str, phone: str, address: str):
    customer = db.query(Customer).filter(Customer.phone == phone).first()
    if customer:
        return customer

    new_customer = Customer(name=name, phone=phone, address=address)
    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)
    return new_customer