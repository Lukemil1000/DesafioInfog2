from fastapi import FastAPI
from win32inetcon import HTTP_STATUS_OK

from DesafioInfog2.schemas.userSchemas import UserCreate, UserPublic

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/auth/register", status_code=HTTP_STATUS_OK, response_model=UserPublic)
def create_user(user: UserCreate):
    return user
