from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from pydantic import BaseModel, field_validator
from datetime import datetime, timezone
import hashlib
from resources.db import get_async_db
from infrastructure.security.hashing import hash_password, verify_password, validate_password_strength
from infrastructure.security.jwt import (
    create_access_token, create_refresh_token, decode_token,
    get_current_user, login_rate_limit,
)
from config.settings import KEY_TOKEN_PASSWORD, KEY_REFRESH_TOKEN
from config.metabase_charts import METABASE_CHARTS
from infrastructure.persistence.repositories.vendedor import VendedorRepository
from infrastructure.persistence.models.vendedor import Vendedor
from infrastructure.persistence.models.token_blacklist import TokenBlacklist
from infrastructure.persistence.models.publicacion import Publicacion

router = APIRouter(prefix="/auth", tags=["auth"])


class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user_id: int
    role: int | str
    email: str
    name: str


class RefreshRequest(BaseModel):
    refresh_token: str


class RefreshResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RegisterRequest(BaseModel):
    email: str
    password: str
    user_name: str | None = None
    nombre_tienda: str | None = None

    @field_validator("password")
    @classmethod
    def validate_password(cls, v):
        validate_password_strength(v)
        return v


class RegisterResponse(BaseModel):
    id: int
    email: str
    user_name: str | None
    role: int | str


class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str

    @field_validator("new_password")
    @classmethod
    def validate_new_password(cls, v):
        validate_password_strength(v)
        return v


@router.post("/login", response_model=LoginResponse)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_async_db),
):
    result = await db.execute(select(Vendedor).where(Vendedor.email == form_data.username))
    user = result.scalar_one_or_none()
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas",
        )
    access_token = create_access_token(
        user_id=str(user.id_vendedor),
        role=getattr(user, 'tipo_plan', 'user'),
        email=user.email,
        name=getattr(user, 'user_name', ''),
    )
    refresh_token = create_refresh_token(
        user_id=str(user.id_vendedor),
        role=getattr(user, 'tipo_plan', 'user'),
        email=user.email,
    )
    return LoginResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        user_id=user.id_vendedor,
        role=getattr(user, 'tipo_plan', 'user'),
        email=user.email,
        name=getattr(user, 'user_name', ''),
    )


@router.post("/register", response_model=RegisterResponse, status_code=status.HTTP_201_CREATED)
async def register(data: RegisterRequest, db: AsyncSession = Depends(get_async_db)):
    result = await db.execute(select(Vendedor).where(Vendedor.email == data.email))
    existing = result.scalar_one_or_none()
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email ya registrado")
    hashed = hash_password(data.password)
    user = Vendedor(
        email=data.email,
        password_hash=hashed,
        user_name=data.user_name or data.email.split('@')[0],
        nombre_tienda=data.nombre_tienda or data.email.split('@')[0],
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return RegisterResponse(
        id=user.id_vendedor,
        email=user.email,
        user_name=getattr(user, 'user_name', None),
        role=getattr(user, 'tipo_plan', 'user'),
    )


@router.post("/refresh", response_model=RefreshResponse)
async def refresh_token(data: RefreshRequest, db: AsyncSession = Depends(get_async_db)):
    payload = decode_token(data.refresh_token, secret=KEY_REFRESH_TOKEN or KEY_TOKEN_PASSWORD)
    token_hash = hashlib.sha256(data.refresh_token.encode()).hexdigest()
    blacklisted = TokenBlacklist(
        token_hash=token_hash,
        expires_at=datetime.fromtimestamp(payload["exp"], tz=timezone.utc),
    )
    db.add(blacklisted)
    await db.commit()
    new_access = create_access_token(
        user_id=payload["sub"], role=payload["role"],
        email=payload.get("email", ""), name=payload.get("name", ""),
    )
    new_refresh = create_refresh_token(
        user_id=payload["sub"], role=payload["role"], email=payload.get("email", ""),
    )
    return RefreshResponse(access_token=new_access, refresh_token=new_refresh)


@router.get("/dashboard")
async def get_dashboard(
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db),
):
    user_id = int(current_user["id"])
    stmt = (
        select(Vendedor)
        .options(
            selectinload(Vendedor.pais_ref),
            selectinload(Vendedor.moneda_ref),
            selectinload(Vendedor.plan_saas_ref),
            selectinload(Vendedor.metricas_reputacion),
            selectinload(Vendedor.metricas_negocio),
            selectinload(Vendedor.metricas_costo),
            selectinload(Vendedor.metricas_stock_full),
            selectinload(Vendedor.metricas_mi_pagina),
            selectinload(Vendedor.reportes_diagnostico),
            selectinload(Vendedor.publicacion).selectinload(Publicacion.rendimiento_publicacion),
            selectinload(Vendedor.publicacion).selectinload(Publicacion.metricas_calidad_publicacion),
        )
        .where(Vendedor.id_vendedor == user_id)
    )
    result = await db.execute(stmt)
    vendedor = result.scalar_one_or_none()
    if not vendedor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vendedor no encontrado")

    def model_to_dict(obj, exclude=None):
        if obj is None:
            return None
        exclude = exclude or set()
        data = {}
        for col in obj.__table__.columns:
            if col.name not in exclude:
                val = getattr(obj, col.name)
                if isinstance(val, datetime):
                    val = val.isoformat()
                data[col.name] = val
        return data

    def pub_to_dict(pub):
        data = model_to_dict(pub, exclude={'id_vendedor'})
        data['rendimiento'] = [model_to_dict(r) for r in (pub.rendimiento_publicacion or [])]
        data['calidad'] = model_to_dict(pub.metricas_calidad_publicacion)
        return data

    metabase_config = METABASE_CHARTS.get(user_id, None)
    response = {
        "vendedor": model_to_dict(vendedor, exclude={'password_hash', 'access_token', 'refresh_token', 'tiempo_token'}),
        "reputacion": model_to_dict(vendedor.metricas_reputacion),
        "negocio": model_to_dict(vendedor.metricas_negocio),
        "costos": model_to_dict(vendedor.metricas_costo),
        "stock_full": model_to_dict(vendedor.metricas_stock_full),
        "mi_pagina": model_to_dict(vendedor.metricas_mi_pagina),
        "publicaciones": [pub_to_dict(p) for p in (vendedor.publicacion or [])],
        "reportes": [model_to_dict(r) for r in (vendedor.reportes_diagnostico or [])],
        "metabase": metabase_config,
    }
    return response


@router.get("/me")
async def get_me(current_user: dict = Depends(get_current_user)):
    return current_user
