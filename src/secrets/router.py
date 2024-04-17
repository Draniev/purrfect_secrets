from fastapi import APIRouter

from src.database import db
from src.secrets.schemas import (SecretAdd, SecretCreated, SecretViewFull,
                                 SecretView)
from src.secrets.services import SecretsCRUD

router = APIRouter(tags=['Secrets'])
secrets_crud = SecretsCRUD(db=db)
is_init = secrets_crud.init_indexes()


@router.get('/secrets', response_model=list[SecretViewFull])
async def get_all():
    result = await secrets_crud.get_all()
    return result


@router.get("/secrets/{secret_key}", response_model=SecretView)
async def get_secret(secret_key: str, secret_pass: str | None = None):
    result = await secrets_crud.get_secret(secret_key, secret_pass)
    return result


@router.post("/generate", response_model=SecretCreated)
async def add_secret(secret: SecretAdd):
    result = await secrets_crud.add_secret(secret)
    return result
