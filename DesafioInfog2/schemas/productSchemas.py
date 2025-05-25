from datetime import datetime

from pydantic import BaseModel, Field


class ProductPublic(BaseModel):
    id: int
    name: str
    description: str
    price: float = Field(gt=0)
    category: str
    stock: int = Field(ge=0)
    expire_date: datetime | None = None

class ProductCreate(BaseModel):
    name: str
    description: str
    price: float = Field(gt=0)
    category: str
    stock: int = Field(ge=0)
    expire_date: datetime | None = None

class ProductList(BaseModel):
    products: list[ProductPublic]