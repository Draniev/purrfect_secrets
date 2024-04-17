from pydantic_settings import BaseSettings


class AppSettings(BaseSettings):
    class Config:
        env_file = '.env'
        env_ignore_empty = True
        extra = "ignore"

    PG_USER: str = 'postgres'
    PG_PASS: str = 'postgres'
    PG_HOST: str = '127.0.0.1'
    PG_NAME: str = 'postgres'
    PG_PORT: str = '5432'

    MO_USER: str = 'root'
    MO_PASS: str = 'example'
    MO_HOST: str = '127.0.0.1'
    MO_PORT: str = '27017'

    KEY: str
    SALT: str

    # SMTP_TLS: bool = True
    # SMTP_SSL: bool = False
    # SMTP_PORT: int = 587
    # SMTP_HOST: str | None = None
    # SMTP_USER: str | None = None
    # SMTP_PASSWORD: str | None = None
    # EMAILS_FROM_EMAIL: str | None = None
    # EMAILS_FROM_NAME: str | None = None


settings = AppSettings()
