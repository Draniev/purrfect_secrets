from datetime import UTC, datetime, timedelta
from typing import Annotated, Optional

from pydantic import BaseModel, BeforeValidator, Field, model_validator
from pydantic.config import ConfigDict
from pydantic.types import PositiveInt

PyObjectId = Annotated[str, BeforeValidator(str)]


class SecretAdd(BaseModel):
    secret_body: str = Field(max_length=65535)
    secret_pass: Optional[str] = None
    lifetime: PositiveInt = 60*60*24*7  # 7 days by default
    expire_at: datetime | None = None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "secret_body": "A very secret message",
                "secret_pass": "example",
                "lifetime": 3600
            }
        },
    )

    @model_validator(mode='after')
    def set_extiration_date(self):
        """
        Sets the expiration date based on the lifetime field.
        If expire_at is provided, it will use that date,
        otherwise, it calculates the expiration date using the lifetime.
        """
        if not self.expire_at:
            self.expire_at = datetime.now(UTC) \
                + timedelta(seconds=self.lifetime)
        return self


class SecretCreated(BaseModel):
    secret_key: str


class SecretView(BaseModel):
    secret_body: str


class SecretViewFull(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    secret_body: str
    secret_pass: Optional[str] = None
    expire_at: datetime | None = None
