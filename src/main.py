from fastapi import FastAPI, HTTPException, status

from src.database import db
from src.secrets.router import router as secrets_router

app = FastAPI(
    title="Trusted Secrets API",
    summary="The app allows you to securely transfer or store sensitive \
             information such as passwords.",
)
app.include_router(secrets_router)


@app.get('/', tags=['Is_ok'])
def hello():
    return {'status': 'i am OK'}
