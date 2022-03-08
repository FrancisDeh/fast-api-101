from datetime import datetime, date
from pydantic import BaseModel, Field, EmailStr, HttpUrl, validator, root_validator
from typing import Optional, List
from fastapi import FastAPI, status, HTTPException

app = FastAPI()


def magic_numbers_factory():
    return [1, 4, 5, 6]


class Person(BaseModel):
    first_name: str = Field(..., min_length=3)
    last_name: str = Field(..., max_length=3)
    email: EmailStr
    website: HttpUrl
    age: Optional[int] = Field(None, ge=0, le=120)
    magic_numbers: List[int] = Field(default_factory=magic_numbers_factory)
    roles: List[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.now)
    birthdate: date

    @validator("birthdate")
    def valid_birthdate(cls, v: date):
        delta = date.today() - v
        age = delta.days / 365
        if age > 120:
            raise ValueError("You seem a bit too old!")
        return v

    def name_dict(self):
        return self.dict(include={"first_name", "last_name"})


class PostBase(BaseModel):
    title: str
    content: str

    def excerpt(self) -> str:
        return f"{self.content[:140]}..."


class PostCreate(PostBase):
    pass


class PostPublic(PostBase):
    id: int


class PostPartialUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None


class PostDB(PostBase):
    id: int
    nb_views: int = 0


class UserRegistration(BaseModel):
    email: EmailStr
    values: List[int]
    password: str
    password_confirmation: str

    @root_validator()
    def validate_password(cls, values):
        password = values.get("password")
        password_confirmation = values.get("password_confirmation")
        if password != password_confirmation:
            raise ValueError("Passwords do not match")
        return values

    @validator("values", pre=True)  # executes before the model is created
    def split_string_values(cls, v):
        if isinstance(v, str):
            return v.split(",")
        return v


# m = UserRegistration(values="1,2,3")
# print(m.values)  # [1, 2, 3]
# m.dict()
# person_include = person.dict(include={"first_name", "last_name"})
# print(person_include)  # {"first_name": "John", "last_name":"Doe"}
# person_exclude = person.dict(exclude={"birthdate","interests"})
# print(person_exclude)

# dummy posts
posts = {
    1: PostDB(id=1, title="The API pitfall", content="hey", nb_views=3)
}


@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=PostPublic)
async def create(post_create: PostCreate):
    new_id = max(posts.keys() or (0,)) + 1
    post = PostDB(id=new_id, **post_create.dict())
    posts[new_id] = post
    return post


@app.patch("/posts/{id}", response_model=PostPublic)
async def partial_update(id: int, post_update: PostPartialUpdate):
    try:
        post_db = posts[id]
        updated_fields = post_update.dict(exclude_unset=True)
        updated_post = post_db.copy(update=updated_fields)
        posts[id] = updated_post
        return updated_post
    except KeyError:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
