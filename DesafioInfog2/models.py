from datetime import datetime
from enum import Enum

from sqlalchemy import func, ForeignKey, Column
from sqlalchemy.orm import registry, Mapped, mapped_column, relationship

table_registry = registry()


class OrderState(str, Enum):
    processing = "processing"
    sent = "sent"
    arrived = "arrived"
    canceled = "canceled"

@table_registry.mapped_as_dataclass
class OrderProduct:
    __tablename__ = "order_product"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    order_id: Mapped[int] = mapped_column("order_id", ForeignKey("orders.id", ondelete="CASCADE"))
    product_id: Mapped[int] = mapped_column("product_id", ForeignKey("products.id"))

@table_registry.mapped_as_dataclass
class User:
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column(unique=True)
    created_at: Mapped[datetime] = mapped_column(init=False, server_default=func.now())

@table_registry.mapped_as_dataclass
class Client:
    __tablename__ = 'clients'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    name: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column(unique=True)
    cpf: Mapped[str] = mapped_column(unique=True)
    orders: Mapped[list["Order"]] = relationship("Order", back_populates="client", init=False)

@table_registry.mapped_as_dataclass
class Product:
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    name: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()
    price: Mapped[float] = mapped_column()
    category: Mapped[str] = mapped_column()
    stock: Mapped[int] = mapped_column()
    expire_date: Mapped[datetime] = mapped_column(nullable=True)
    orders: Mapped[list["Order"]] = relationship(
        "Order", secondary="order_product", back_populates="products", init=False
    )

@table_registry.mapped_as_dataclass
class Order:
    __tablename__ = 'orders'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    state: Mapped[OrderState] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(init=False, server_default=func.now())
    products: Mapped[list[Product]] = relationship(
        "Product", secondary="order_product", back_populates="orders"
    )
    client_id: Mapped[int] = mapped_column(ForeignKey("clients.id"))
    client: Mapped[Client] = relationship("Client", back_populates="orders", init=False)
