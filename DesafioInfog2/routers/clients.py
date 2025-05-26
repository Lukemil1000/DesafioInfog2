from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from DesafioInfog2.database import get_session
from DesafioInfog2.models import User, Client
from DesafioInfog2.schemas.clientSchemas import ClientPublic, ClientCreate, ClientList
from DesafioInfog2.schemas.utilSchemas import Message
from DesafioInfog2.security import get_token_user

def check_existing_client(session: Session, client: ClientCreate, client_id: int | None = None):
    query = select(Client).where(
        (Client.email == client.email) | (Client.cpf == client.cpf)
    )

    if client_id:
        query = query.where(Client.id != client_id)

    existing_client = session.scalar(query)

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

router = APIRouter(prefix='/clients', tags=['clients'])

@router.post("/", status_code=HTTPStatus.CREATED, response_model=ClientPublic)
def create_client(
        client: ClientCreate,
        session: Session = Depends(get_session),
        token_user: User = Depends(get_token_user)
):
    check_existing_client(session, client)

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
        skip: int = Query(default=0, ge=0),
        limit: int = Query(default=10, gt=0),
        name: str | None = Query(default=None),
        email: str | None = Query(default=None),
        session: Session = Depends(get_session),
        token_user: User = Depends(get_token_user)
):
    query = select(Client)

    if name:
        query = query.filter(Client.name.contains(name))
    if email:
        query = query.filter(Client.email.contains(email))

    clients = session.scalars(query.offset(skip).limit(limit)).all()

    return {"clients": clients}

@router.get("/{client_id}", status_code=HTTPStatus.OK, response_model=ClientPublic)
def get_client_by_id(
        client_id: int,
        session: Session = Depends(get_session),
        token_user: User = Depends(get_token_user)
):
    client = session.scalar(select(Client).where(Client.id == client_id))

    if not client:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Client not found"
        )

    return client

@router.delete("/{client_id}", status_code=HTTPStatus.OK, response_model=Message)
def delete_client(
        client_id: int,
        session: Session = Depends(get_session),
        token_user: User = Depends(get_token_user)
):
    client = session.scalar(select(Client).where(Client.id == client_id))

    if not client:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Client not found"
        )

    session.delete(client)
    session.commit()

    return {"message": "Client deleted"}

@router.put("/{client_id}", status_code=HTTPStatus.OK, response_model=ClientPublic)
def update_client(
        client_update: ClientCreate,
        client_id: int,
        session: Session = Depends(get_session),
        token_user: User = Depends(get_token_user)
):
    client = session.scalar(select(Client).where(Client.id == client_id))

    if not client:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Client not found"
        )

    check_existing_client(session, client_update, client_id=client_id)

    client.name = client_update.name
    client.email = client_update.email
    client.cpf = client_update.cpf

    session.add(client)
    session.commit()
    session.refresh(client)

    return client