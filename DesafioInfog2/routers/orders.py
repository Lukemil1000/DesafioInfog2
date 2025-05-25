from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from DesafioInfog2.database import get_session
from DesafioInfog2.models import User, Product, Order
from DesafioInfog2.schemas.orderSchemas import OrderCreate, OrderPublic
from DesafioInfog2.securiry import get_token_user

router = APIRouter(prefix='/orders', tags=['orders'])

@router.post('/', status_code=HTTPStatus.CREATED, response_model=OrderPublic)
def create_order(
        order: OrderCreate,
        session: Session = Depends(get_session),
        token_user: User = Depends(get_token_user)
):
    order_products = []
    for product_id in order.products:
        found_product = session.scalar(select(Product).where(Product.id == product_id))

        if not found_product:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=f'Product with id {product_id} not found')

        order_products.append(found_product)

    db_order = Order(
        state=order.state,
        products=order_products
    )

    session.add(db_order)
    session.commit()
    session.refresh(db_order)

    return db_order