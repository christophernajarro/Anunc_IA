from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional

# Esquema para la solicitud de registro
class RegisterRequest(BaseModel):
    nombre: str = Field(..., example="Juan Pérez")
    email: EmailStr = Field(..., example="juan.perez@example.com")
    password: str = Field(..., min_length=6, example="strongpassword")


# Esquema para la respuesta de registro
class RegisterResponse(BaseModel):
    msg: str = Field(..., example="Usuario registrado con éxito")

# Esquema para la respuesta de login
class LoginResponse(BaseModel):
    access_token: str
    token_type: str

# Esquema para el usuario
class UsuarioBase(BaseModel):
    id_usuario: int
    nombre: str
    email: EmailStr
    fecha_registro: datetime

    model_config = {
        "from_attributes": True
    }


# Esquema para la creación de usuario (opcional, si deseas separar la creación)
class UsuarioCreate(BaseModel):
    nombre: str
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
