from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from DesafioInfog2.database import get_session
from DesafioInfog2.models import User, Product
from DesafioInfog2.schemas.productSchemas import ProductPublic, ProductCreate, ProductList
from DesafioInfog2.securiry import get_token_user

router = APIRouter(prefix='/products', tags=['products'])

@router.post("/", status_code=HTTPStatus.CREATED, response_model=ProductPublic)
def create_product(
        product: ProductCreate,
        session: Session = Depends(get_session),
        token_user: User = Depends(get_token_user)
):
    db_product = Product(
        name=product.name,
        description=product.description,
        price=product.price,
        category=product.category,
        stock=product.stock,
        expire_date=product.expire_date,
    )

    session.add(db_product)
    session.commit()
    session.refresh(db_product)

    return db_product

@router.get("/", response_model=ProductList)
def get_products(
        skip: int = 0,
        limit: int = 10,
        category: str | None = None,
        price_min: float | None = None,
        price_max: float | None = None,
        available_stock: bool | None = None,
        session: Session = Depends(get_session),
        token_user: User = Depends(get_token_user)
):
    query = select(Product)

    if category:
        query = query.filter(Product.category == category)
    if price_min:
        query = query.filter(Product.price >= price_min)
    if price_max:
        query = query.filter(Product.price <= price_max)
    if available_stock is not None:
        if available_stock:
            query = query.filter(Product.stock > 0)
        else:
            query = query.filter(Product.stock == 0)

    products = session.scalars(query.offset(skip).limit(limit)).all()

    return {"products": products}