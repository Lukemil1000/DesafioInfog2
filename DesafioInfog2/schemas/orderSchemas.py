from datetime import datetime

from pydantic import BaseModel, Field

from DesafioInfog2.models import OrderState
from DesafioInfog2.schemas.productSchemas import ProductList


class OrderPublic(BaseModel):
    id: int
    state: OrderState
    created_at: datetime
    products: ProductList

class OrderCreate(BaseModel):
    state: OrderState
    products: list[int]

class OrderList(BaseModel):
    orders: list[OrderPublic]
