from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from DesafioInfog2.database import get_session
from DesafioInfog2.models import User, Product
from DesafioInfog2.schemas.productSchemas import ProductPublic, ProductCreate
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