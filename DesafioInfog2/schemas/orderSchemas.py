from datetime import datetime

from pydantic import BaseModel

from DesafioInfog2.models import OrderState
from DesafioInfog2.schemas.productSchemas import ProductPublic


class OrderPublic(BaseModel):
    id: int
    state: OrderState
    created_at: datetime
    products: list[ProductPublic]
    client_id: int

class OrderCreate(BaseModel):
    state: OrderState
    products: list[int]
    client_id: int

class OrderList(BaseModel):
    orders: list[OrderPublic]
