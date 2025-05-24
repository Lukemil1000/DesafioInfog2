from pydantic import BaseModel, EmailStr

class Token(BaseModel):
    access_token: str
    token_type: str

class UserCreate(BaseModel):
    username: str
    password: str
    email: EmailStr

class UserPublic(BaseModel):
    username: str
    email: EmailStr