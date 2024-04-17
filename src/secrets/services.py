from bson import ObjectId
from fastapi import HTTPException, status
from motor.motor_asyncio import AsyncIOMotorDatabase

from src.secrets.schemas import (SecretAdd, SecretCreated, SecretFull,
                                 SecretsCollection, SecretView)


class SecretsCRUD:
    def __init__(self, db: AsyncIOMotorDatabase) -> None:
        self.db = db
        self.collection = db['secrets_collection']
        self.is_init_indexes: bool = False

    async def init_indexes(self):
        # Creates an index for deleting a document after the date has expired
        await self.collection.create_index('expire_at', expireAfterSeconds=0)

    async def add_secret(self,
                         secret: SecretAdd
                         ) -> SecretCreated:
        """
        Saves the secret in the database.
        On input: secret body, password (optional), lifetime (optional)
        Output: key to access the secret
        """

        # Учитывая необходимость работать с асинхронным драйвером БД Монго
        # я голову сломал как красивее всего сделать инициализацию индексов
        # для настройки TTL, но, тщетно. Казалось бы, индексы надо один раз
        # установить на нужные коллекции, но... в SQL я бы это сделал
        # в миграциях, с синхронным драйвером - в __init__.
        # Были и другие варианты, но этот мне показался лучшим!
        if not self.is_init_indexes:
            await self.init_indexes()
            self.is_init_indexes = True

        # server = await self.db.client.server_info()
        # print(f'server info: {server}')
        # print(f'new secret: {secret.model_dump()}')
        result = await self.collection.insert_one(
            secret.model_dump(exclude={'lifetime'})
        )
        result_id: str = str(result.inserted_id)
        return SecretCreated(secret_key=result_id)

    async def get_secret(self,
                         key: str,
                         passw: str | None = None
                         ) -> SecretView:
        """
        Gets the secret from the database.
        On input: secret key and password (optional)
        Output: secret body or 404.
        You can get the secret only once,
        after that it is deleted from the database.
        """

        result = await self.collection.find_one_and_delete(
            {'_id': ObjectId(key)}
        )
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Secret not found!")
        return SecretView(**result)

    async def get_all(self) -> SecretsCollection:
        """
        Performs a decorative function.
        For debugging purposes only: displays the state
        of the database as it is.
        """
        secrets = await self.collection.find().to_list(1000)
        return SecretsCollection(secrets=secrets)
