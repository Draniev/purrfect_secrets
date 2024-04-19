from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.database import open_mongo_db, close_mongo_db
from src.secrets.router import router as secrets_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await open_mongo_db()
    print('ВЫПОЛНЕНА ИНИЦИАЛИЗАЦИЯ БД')
    yield
    await close_mongo_db()
    print('БАЗА ДАННЫХ ЗАКРЫТА')


app = FastAPI(
    lifespan=lifespan,
    title="Trusted Secrets API",
    summary="The app allows you to securely transfer or store sensitive \
             information such as passwords.",
)
app.include_router(secrets_router)


@app.get('/', tags=['Is_ok'])
def hello():
    return {'status': 'i am OK'}
