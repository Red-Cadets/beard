from fastapi import FastAPI
import logging
import uvicorn

from config import get_config
from db import db
from api import router as api_router

app = FastAPI()

app.include_router(api_router, prefix='/api', tags=['api'])

config = get_config()

logger = logging.getLogger("uvicorn")


@app.on_event("startup")
async def startup():
    await db.connect_to_database(
        path=f"mongodb://{config.MONGO_USER}:{config.MONGO_PASS}@{config.MONGO_HOST}:{config.MONGO_PORT}/")

if __name__ == '__main__':
    uvicorn.run("app:app", host="0.0.0.0", port=8888,
                reload=config.DEBUG, workers=4)
