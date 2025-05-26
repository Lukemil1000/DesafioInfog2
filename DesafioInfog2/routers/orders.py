from datetime import datetime
from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from DesafioInfog2.database import get_session
from DesafioInfog2.models import User, Product, Order, OrderState, Client
from DesafioInfog2.schemas.orderSchemas import OrderCreate, OrderPublic, OrderList
from DesafioInfog2.schemas.utilSchemas import Message
from DesafioInfog2.security import get_token_user

router = APIRouter(prefix='/orders', tags=['orders'])

@router.post('/', status_code=HTTPStatus.CREATED, response_model=OrderPublic)
def create_order(
        order: OrderCreate,
        session: Session = Depends(get_session),
        token_user: User = Depends(get_token_user)
):
    found_client = session.scalar(select(Client).where(Client.id == order.client_id))

    if not found_client:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=f'Client with id {order.client_id} not found')

    if order.products != set(order.products):
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail=f'Product repeat not allowed')

    order_products = []
    for product_id in order.products:
        found_product = session.scalar(select(Product).where(Product.id == product_id))

        if not found_product:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=f'Product with id {product_id} not found')

        order_products.append(found_product)

    db_order = Order(
        state=order.state,
        products=order_products,
        client_id=order.client_id
    )

    session.add(db_order)
    session.commit()
    session.refresh(db_order)

    return db_order

@router.get('/', status_code=HTTPStatus.OK, response_model=OrderList)
def get_orders(
        skip: int = Query(default=0, ge=0),
        limit: int = Query(default=10, gt=0),
        state: OrderState | None = Query(default=None),
        date_min: datetime | None = Query(default=None),
        date_max: datetime | None = Query(default=None),
        session: Session = Depends(get_session),
        token_user: User = Depends(get_token_user)
):
    query = select(Order)

    if state:
        query = query.filter(Order.state == state)
    if date_min:
        query = query.filter(Order.created_at >= date_min)
    if date_max:
        query = query.filter(Order.created_at <= date_max)

    orders = session.scalars(query.offset(skip).limit(limit)).all()

    return {"orders": orders}

@router.get('/{order_id}', status_code=HTTPStatus.OK, response_model=OrderPublic)
def get_order_by_id(
        order_id: int,
        session: Session = Depends(get_session),
        token_user: User = Depends(get_token_user)
):
    order = session.scalar(select(Order).where(Order.id == order_id))

    if not order:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f'Order not found'
        )

    return order

@router.delete('/{order_id}', status_code=HTTPStatus.OK, response_model=Message)
def delete_order(
        order_id: int,
        session: Session = Depends(get_session),
        token_user: User = Depends(get_token_user)
):
    order = session.scalar(select(Order).where(Order.id == order_id))

    if not order:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f'Order not found'
        )

    session.delete(order)
    session.commit()

    return {"message": "Order deleted"}

@router.put('/{order_id}', status_code=HTTPStatus.OK, response_model=OrderPublic)
def update_order(
        order_update: OrderCreate,
        order_id: int,
        session: Session = Depends(get_session),
        token_user: User = Depends(get_token_user)
):
    order = session.scalar(select(Order).where(Order.id == order_id))

    if not order:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f'Order not found'
        )

    found_client = session.scalar(select(Client).where(Client.id == order_update.client_id))

    if not found_client:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=f'Client with id {order_update.client_id} not found')

    if order_update.products != set(order_update.products):
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail=f'Product repeat not allowed')

    order_products = []
    for product_id in order_update.products:
        found_product = session.scalar(select(Product).where(Product.id == product_id))

        if not found_product:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=f'Product with id {product_id} not found')

        order_products.append(found_product)

    order.state = order_update.state
    order.products = order_products
    order.client_id = order_update.client_id

    session.add(order)
    session.commit()
    session.refresh(order)

    return order