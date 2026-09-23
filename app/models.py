from pydantic import BaseModel, EmailStr


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    status: str
    token: str
    role: str


class DonacionCreate(BaseModel):
    donante: str
    tipo: str
    cantidad_kg: float


class DonacionResponse(BaseModel):
    id: str
    donante: str
    tipo: str
    cantidad_kg: float
    estatus: str
