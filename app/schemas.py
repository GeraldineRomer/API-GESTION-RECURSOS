from pydantic import BaseModel, EmailStr, field_validator
from datetime import datetime
from typing import Optional


# ---------- Schemas de Usuario ----------

class UserCreate(BaseModel):
    """Lo que el cliente envía para registrarse"""
    email: EmailStr
    password: str
    full_name: Optional[str] = None
    
    @field_validator("password")
    @classmethod
    def password_length(cls, v):
        if len(v) < 8:
            raise ValueError("La contraseña debe tener al menos 8 caracteres")
        if len(v) > 72:
            raise ValueError("La contraseña no puede superar 72 caracteres")
        return v


class UserResponse(BaseModel):
    """Lo que la API responde — nunca incluye la contraseña"""
    id: int
    email: EmailStr
    full_name: Optional[str] = None
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True  # permite convertir desde un objeto SQLAlchemy


# ---------- Schemas de Autenticación ----------

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


# ---------- Schemas de Item ----------

class ItemCreate(BaseModel):
    title: str
    description: Optional[str] = None


class ItemResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    created_at: datetime
    owner_id: int

    class Config:
        from_attributes = True
