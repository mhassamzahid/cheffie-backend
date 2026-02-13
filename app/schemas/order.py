from pydantic import BaseModel
from typing import List, Dict

class OrderCreate(BaseModel):
    phone: str
    name: str
    address: str
    items: List[Dict]

class OrderUpdate(BaseModel):
    items: List[Dict]