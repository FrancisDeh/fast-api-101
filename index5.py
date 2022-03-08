from fastapi import FastAPI, Depends, status, HTTPException, Query, Header
from pydantic import BaseModel
from typing import Tuple, Optional

app = FastAPI()


class Post(BaseModel):
    title: str


posts = {
    1: Post(title="The API pitfall")
}


async def pagination(skip: int = 0, limit: int = 10) -> Tuple[int, int]:
    return skip, limit


@app.get("/items")
async def items(p: Tuple[int, int] = Depends(pagination)):
    skip, limit = p
    return {"skip": skip, "limit": limit}


async def get_post_or_404(id: int) -> Post:
    try:
        return posts[id]
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@app.get("/posts/{id}")
async def get(post: Post = Depends(get_post_or_404)):
    return post


class Pagination:
    def __init__(self, maximum_limit: int = 100):
        self.maximum_limit = maximum_limit

    async def __call__(self, skip: int = Query(0, ge=0), limit: int = Query(10, ge=0), ) -> Tuple[int, int]:
        capped_limit = min(self.maximum_limit, limit)
        return skip, capped_limit


page = Pagination(maximum_limit=50)


@app.get("/item2s")
async def items2(p: Tuple[int, int] = Depends(page)):
    skip, limit = p
    return {"skip": skip, "limit": limit}


def secret_header(secret_header: Optional[str] = Header(None)) -> None:
    if not secret_header or secret_header != "SECRET_VALUE":
        raise HTTPException(status.HTTP_403_FORBIDDEN)


@app.get("/protected-route", dependencies=[Depends(secret_header)])
async def protected_route():
    return {"hello": "world"}
