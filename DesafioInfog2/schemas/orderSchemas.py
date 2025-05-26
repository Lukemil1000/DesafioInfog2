from datetime import datetime

from pydantic import BaseModel, Field

from DesafioInfog2.models import OrderState
from DesafioInfog2.schemas.productSchemas import ProductPublic


class OrderPublic(BaseModel):
    id: int
    state: OrderState
    created_at: datetime
    products: list[ProductPublic] = Field(min_length=1)
    client_id: int

class OrderCreate(BaseModel):
    state: OrderState
    products: list[int] = Field(min_length=1)
    client_id: int

class OrderList(BaseModel):
    orders: list[OrderPublic]
