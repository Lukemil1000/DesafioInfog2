from pydantic import BaseModel, EmailStr
from pydantic_br import CPFMask

class CPFMaskCustom(CPFMask):
    examples = "000.000.000-00"

class ClientPublic(BaseModel):
    id: int
    name: str
    email: EmailStr
    cpf: CPFMaskCustom

class ClientCreate(BaseModel):
    name: str
    email: EmailStr
    cpf: CPFMaskCustom

class ClientList(BaseModel):
    clients: list[ClientPublic]