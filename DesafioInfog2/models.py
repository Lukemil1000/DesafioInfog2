from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import registry, Mapped, mapped_column

table_registry = registry()

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