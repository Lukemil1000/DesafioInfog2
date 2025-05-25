from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from DesafioInfog2.database import get_session
from DesafioInfog2.models import User, Product
from DesafioInfog2.schemas.productSchemas import ProductPublic, ProductCreate, ProductList
from DesafioInfog2.schemas.utilSchemas import Message
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

@router.get("/", status_code=HTTPStatus.OK, response_model=ProductList)
def get_products(
        skip: int = Query(default=0, ge=0),
        limit: int = Query(default=10, gt=0),
        category: str | None = Query(default=None),
        price_min: float | None = Query(default=None, ge=0),
        price_max: float | None = Query(default=None, ge=0),
        available_stock: bool | None = Query(default=None),
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

@router.get("/{product_id}", status_code=HTTPStatus.OK, response_model=ProductPublic)
def get_product_by_id(
        product_id: int,
        session: Session = Depends(get_session),
        token_user: User = Depends(get_token_user)
):
    product = session.scalar(select(Product).where(Product.id == product_id))

    if not product:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Product not found"
        )

    return product

@router.delete("/{product_id}", status_code=HTTPStatus.OK, response_model=Message)
def delete_product(
        product_id: int,
        session: Session = Depends(get_session),
        token_user: User = Depends(get_token_user)
):
    product = session.scalar(select(Product).where(Product.id == product_id))

    if not product:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Product not found"
        )

    session.delete(product)
    session.commit()

    return {"message": "Product deleted"}

