from fastapi import FastAPI, status
from pydantic import BaseModel
from typing import Any

app = FastAPI()


class Post(BaseModel):
    title: str


@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_post(post: Post) -> Any:
    return post
