from fastapi import APIRouter, Depends, status

from src.secrets.dependencies import secrets_crud
from src.secrets.schemas import (SecretAdd, SecretCreated, SecretView,
                                 SecretViewFull)
from src.secrets.services import SecretsCRUD

router = APIRouter(tags=["Secrets"])


@router.get(
    "/secrets",
    response_description="This feature is for demonstration purposes only. \
                          Shows all documents in the database as they are \
                          (encrypted)",
    summary="Shows all documents in the database as they are",
    response_model_by_alias=False,
    response_model_exclude_unset=True,
    response_model=list[SecretViewFull],
)
async def get_all(
        crud: SecretsCRUD = Depends(secrets_crud),
        ):
    result = await crud.get_all()
    return result


@router.get(
    "/secrets/{secret_key}",
    response_description="Shows a stored secret. After displaying the \
                          secret, it is immediately deleted.",
    summary="Shows a stored secret and then delete it.",
    response_model=SecretView,
)
async def get_secret(
        secret_key: str,
        secret_pass: str | None = None,
        crud: SecretsCRUD = Depends(secrets_crud),
        ):
    result = await crud.get_secret(secret_key, secret_pass)
    return result


@router.post(
    "/generate",
    response_description="Stores the new secret in the database. \
                          If no password is specified, the secret will \
                          still be encrypted in the database. But the key \
                          will be sufficient for displaying.",
    summary="Stores the new secret in the database.",
    status_code=status.HTTP_201_CREATED,
    response_model=SecretCreated,
)
async def add_secret(
        secret: SecretAdd,
        crud: SecretsCRUD = Depends(secrets_crud),
        ):
    result = await crud.add_secret(secret)
    return result
