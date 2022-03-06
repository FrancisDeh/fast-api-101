from typing import Any

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def hello_world() -> Any:
    return {"hello": "world"}
