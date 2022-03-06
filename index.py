from enum import Enum
from typing import Any
from fastapi import FastAPI, Path, Query, Body
from pydantic import BaseModel

app = FastAPI()


class User(BaseModel):
    name: str
    age: int


class Company(BaseModel):
    name: str


class UserType(str, Enum):
    STANDARD = "standard"
    ADMIN = "admin"


@app.get("/")
async def hello_world() -> Any:
    return {"hello": "world"}


@app.get("/users/{id}")
async def get_user_by_id(id: int = Path(..., ge=1)):
    return {"id": id}


@app.get("/users/{type}/{id}")
async def get_user_by_type_and_id(type: UserType, id: int) -> Any:
    return {"type": type, "id": id}


@app.get("/users")
async def get_users(page: int = 1, size: int = 10) -> Any:
    return {"page": page, "size": size}


@app.get("/users2")
async def get_users2(page: int = Query(1, gt=0), size: int = Query(10, le=1000)) -> Any:
    return {"page": page, "size": size}


@app.post("/users")
async def create_user(name: str = Body(...), age: int = Body(...)) -> Any:
    return {"name": name, "age": age}


@app.post("/users2")
async def create_user2(user: User, company: Company) -> Any:
    return {"user": user, "company": company}


@app.get("/licence-plates/{licence}")
async def get_licence_plate(licence: str = Path(..., min_length=9, max_length=9, regex=r"^\w{2}-\d{3}-\w{2}$")) -> Any:
    return {"licence": licence}
