from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy import select

from DesafioInfog2.database import get_session
from DesafioInfog2.models import User
from DesafioInfog2.schemas.userSchemas import UserPublic, UserCreate
from DesafioInfog2.schemas.utilSchemas import Token
from DesafioInfog2.security import hash_password, verify_password, create_access_token, get_token_user

router = APIRouter(prefix='/auth', tags=['auth'])


@router.post("/register", status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserCreate, session: Session = Depends(get_session)):
    existing_user = session.scalar(
        select(User).where(
            (User.username == user.username) | (User.email == user.email)
        )
    )

    if existing_user:
        if existing_user.username == user.username:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail="Username already registered"
            )
        elif existing_user.email == user.email:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail="Email already registered"
            )

    hashed_password = hash_password(user.password)

    db_user = User(
        username=user.username,
        password=hashed_password,
        email=user.email
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user

@router.post("/login", status_code=HTTPStatus.OK, response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    user = session.scalar(select(User).where(User.username == form_data.username))

    if not user:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Incorrect username or password"
        )

    if not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Incorrect username or password"
        )

    token = create_access_token(data={"sub": user.username})

    return {"access_token": token, "token_type": "bearer"}

@router.post("/refresh-token", status_code=HTTPStatus.OK, response_model=Token)
def refresh_token(token_user: User = Depends(get_token_user)):
    token = create_access_token(data={"sub": token_user.username})

    return {"access_token": token, "token_type": "bearer"}