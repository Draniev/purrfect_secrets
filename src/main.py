from fastapi import FastAPI, HTTPException, status

from src.database import db
from src.secrets.router import router as secrets_router

collection = db['test_collection']

app = FastAPI(
    title="Trusted Secrets API",
    summary="The app allows you to securely transfer or store sensitive \
             information such as passwords.",
)
app.include_router(secrets_router)


@app.get('/', tags=['is_ok'])
def hello():
    return {'status': 'i am OK'}


@app.get('/test/{title}', tags=['test'])
async def test_get(title: str):
    result = await collection.find_one({"title": title})
    print(result)
    if not result:
        raise HTTPException(status_code=404, detail='Secret not found')
    return {
        'status': status.HTTP_200_OK,
        'result': repr(result)
    }


@app.post('/test', status_code=status.HTTP_201_CREATED, tags=['test'])
async def test_post(data_dict: dict):
    result = await collection.insert_one(data_dict)
    return {
        'status': status.HTTP_201_CREATED,
        'obj_id': repr(result.inserted_id)
    }
