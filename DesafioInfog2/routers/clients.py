from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from DesafioInfog2.database import get_session
from DesafioInfog2.models import User, Client
from DesafioInfog2.schemas.clientSchemas import ClientPublic, ClientCreate, ClientList
from DesafioInfog2.securiry import get_token_user

router = APIRouter(prefix='/clients', tags=['clients'])

@router.post("/", status_code=HTTPStatus.CREATED, response_model=ClientPublic)
def create_client(
        client: ClientCreate,
        session: Session = Depends(get_session),
        token_user: User = Depends(get_token_user)
):
    existing_client = session.scalar(
        select(Client).where(
            (Client.email == client.email) | (Client.cpf == client.cpf)
        )
    )

    if existing_client:
        if existing_client.email == client.email:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail="Email already registered"
            )
        elif existing_client.cpf == client.cpf:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail="CPF already registered"
            )

    db_client = Client(
        name=client.name,
        email=client.email,
        cpf=client.cpf
    )

    session.add(db_client)
    session.commit()
    session.refresh(db_client)

    return db_client

@router.get("/", status_code=HTTPStatus.OK, response_model=ClientList)
def get_clients(
        skip: int = 0,
        limit: int = 10,
        session: Session = Depends(get_session),
        token_user: User = Depends(get_token_user)
):
    clients = session.scalars(select(Client).offset(skip).limit(limit)).all()

    return {"clients": clients}