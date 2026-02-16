from fastapi import FastAPI
from app.core.database import Base, engine
from app.routers import customers, orders
from mangum import Mangum

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Restaurant Voice Agent API")

app.include_router(customers.router)
app.include_router(orders.router)


@app.get("/health")
def health():
    return {"status": "running"}

# AWS Lambda handler

from mangum import Mangum

handler = Mangum(app)