from bson import ObjectId
from fastapi import HTTPException, status
from motor.motor_asyncio import AsyncIOMotorClient

from src.config import settings as s
from src.secrets.cipherer import Cipherer
from src.secrets.schemas import (SecretAdd, SecretCreated, SecretView,
                                 SecretViewFull)


class SecretsCRUD:
    def __init__(self, conn: AsyncIOMotorClient) -> None:
        self.conn = conn
        self.collection = conn[s.MO_DBNAME][s.secrets_collection]
        self.cipherer = Cipherer()

    def encrypt_secret(self, secret: SecretAdd) -> SecretAdd:
        password = secret.secret_pass
        encrypted_body = self.cipherer.encrypt(secret.secret_body, password)
        return SecretAdd(
            secret_body=encrypted_body,
            expire_at=secret.expire_at,
        )

    async def add_secret(self,
                         secret: SecretAdd
                         ) -> SecretCreated:
        """
        Saves the secret in the database.
        On input: secret body, password (optional), lifetime (optional)
        Output: key to access the secret
        """
        encrypted: SecretAdd = self.encrypt_secret(secret)
        result = await self.collection.insert_one(
            encrypted.model_dump(exclude={'lifetime', 'secret_pass'})
        )
        result_id: str = str(result.inserted_id)
        encrypted_id = self.cipherer.encrypt(result_id)

        return SecretCreated(secret_key=encrypted_id)

    async def get_secret(self,
                         encrypt_key: str,
                         passw: str | None = None
                         ) -> SecretView:
        """
        Gets the secret from the database.
        On input: secret key and password (optional)
        Output: secret body or 404.
        You can get the secret only once,
        after that it is deleted from the database.
        """
        decrypted_key, is_ok = self.cipherer.decrypt(encrypt_key)
        if not is_ok:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Key data is corrupted"
            )

        result = await self.collection.find_one(
            {'_id': ObjectId(decrypted_key)}
        )
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Secret not found!"
            )

        decr_body, is_ok = self.cipherer.decrypt(result['secret_body'], passw)
        if not is_ok:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Password is invalid or corrupted"
            )

        result = await self.collection.delete_one(
            {'_id': ObjectId(decrypted_key)}
        )
        return SecretView(secret_body=decr_body)

    async def get_all(self) -> list[SecretViewFull]:
        """
        Performs a decorative function.
        For debugging purposes only: displays the state
        of the database as it is.
        """
        secrets = await self.collection.find().to_list(1000)
        return secrets
