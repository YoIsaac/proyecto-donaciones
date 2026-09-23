from datetime import datetime, timedelta
from typing import List, Optional

import jwt
from fastapi import Depends, FastAPI, Header, HTTPException, status
from pydantic import BaseModel, EmailStr

SECRET_KEY = "secreto_super_seguro_tecmilenio_2026"
ALGORITHM = "HS256"

app = FastAPI(
    title="Sistema de Gestión de Donaciones - Red Solidaria",
    version="1.0.0",
    description="API RESTful con autenticación JWT, RBAC y gestión de recursos.",
)

USERS_DB = {
    "admin@redsolidaria.org": {
        "id": "USR-001",
        "email": "admin@redsolidaria.org",
        "password": "PasswordSegura123!",
        "role": "ADMIN",
    },
    "donante@empresa.com": {
        "id": "USR-002",
        "email": "donante@empresa.com",
        "password": "Password123!",
        "role": "USUARIO",
    },
}

DONATIONS_DB = [
    {
        "id": "DON-1001",
        "donante": "Empresa Alimentos S.A.",
        "tipo": "Alimentos no perecederos",
        "cantidad_kg": 350.5,
        "estatus": "Completado",
    }
]


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


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(hours=2))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user_role(authorization: str = Header(...)) -> str:
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Header Authorization inválido. Debe usar formato Bearer",
        )

    token = authorization.split(" ", 1)[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        role: str = payload.get("role")
        if role is None:
            raise HTTPException(status_code=401, detail="Token no contiene rol")
        return role
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token inválido")


@app.get("/")
def read_root():
    return {"message": "API de Gestión de Donaciones activa"}


@app.post("/api/auth/login", response_model=TokenResponse)
def login(credentials: LoginRequest):
    user = USERS_DB.get(credentials.email)
    if not user or user["password"] != credentials.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
        )

    token = create_access_token({"sub": user["email"], "role": user["role"]})
    return {"status": "success", "token": token, "role": user["role"]}


@app.get("/api/donaciones", response_model=List[DonacionResponse])
def listar_donaciones(role: str = Depends(get_current_user_role)):
    return DONATIONS_DB


@app.post("/api/donaciones", response_model=DonacionResponse, status_code=201)
def registrar_donacion(donacion: DonacionCreate, role: str = Depends(get_current_user_role)):
    if role != "ADMIN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acceso denegado. Se requieren permisos de Administrador.",
        )

    nueva_donacion = {
        "id": f"DON-{len(DONATIONS_DB) + 1001}",
        "donante": donacion.donante,
        "tipo": donacion.tipo,
        "cantidad_kg": donacion.cantidad_kg,
        "estatus": "Registrado",
    }
    DONATIONS_DB.append(nueva_donacion)
    return nueva_donacion
