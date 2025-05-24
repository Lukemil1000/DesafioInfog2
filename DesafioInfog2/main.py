from fastapi import FastAPI, Depends, HTTPException
from http import HTTPStatus

from sqlalchemy import select
from sqlalchemy.orm import Session

from DesafioInfog2.models import User
from DesafioInfog2.schemas.userSchemas import UserCreate, UserPublic
from DesafioInfog2.database import get_session
from DesafioInfog2.securiry import hash_password

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/auth/register", status_code=HTTPStatus.CREATED, response_model=UserPublic)
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
