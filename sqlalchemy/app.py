from fastapi import FastAPI
from database import database, sqlalchemy_engine
from sqlalchemy.models import metadata

app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()
    metadata.create_all(sqlalchemy_engine)


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
