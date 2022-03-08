from os import path
from fastapi import FastAPI, status, Path, Body, HTTPException
from pydantic import BaseModel
from typing import Any

from starlette.responses import Response, HTMLResponse, PlainTextResponse, RedirectResponse, FileResponse

app = FastAPI()


class Post(BaseModel):
    title: str
    nb_views: int


class PostResponse(BaseModel):
    title: str


# dummy posts
posts = {
    1: Post(title="The API pitfall", nb_views=3)
}


@app.get("/")
async def home(response: Response):
    response.set_cookie("cookie-name", "cookie-value", max_age=86400)
    response.headers['Custom-Header'] = "Custom-Header-Value"
    return {"hello": "World"}


@app.get("/posts")
async def posts() -> Any:
    return posts


@app.get("/posts/{id}", response_model=PostResponse)
async def get_post(id: int):
    return posts[id]


@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_post(post: Post) -> Any:
    return post


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int = Path(...)) -> Any:
    posts.pop(id, None)
    return None


@app.put("/posts/{id}")
async def update_or_create_post(id: int, post: Post, response: Response):
    if id not in posts:
        response.status_code = status.HTTP_201_CREATED
    posts[id] = post
    return posts[id]


@app.post("/password")
async def check_password(password: str = Body(...), password_confirm: str = Body(...)):
    if password != password_confirm:
        # raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Passwords don't match")
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail={
            "message": "Passwords don't match",
            "hints": ["Make sure keyboard caps is off", "Check that the length are the same"]
        })
    return {"message": "Passwords match"}


@app.get("/html", response_class=HTMLResponse)
async def get_html():
    return """
    <html>
    <head><title>Hello world!</title></head>
    <body><h1>Hello world!</h1></body>
    </html>
    """


@app.get("/text", response_class=PlainTextResponse)
async def text():
    return "Hello world!"


@app.get("/redirect")
async def redirect():
    return RedirectResponse("/new-url")
    # return RedirectResponse("/new-url", status_code=status.HTTP_301_MOVED_PERMANENTLY)


@app.get("/download-file")
async def download_file():
    directory = path.dirname(path.dirname(__file__))
    file = path.join(directory, "", "command.txt")
    return FileResponse(file)


@app.get("/xml")
async def get_xml():
    content = """<?xml version="1.0" encoding="UTF-8"?>
        <Hello>World</Hello>
        """
    return Response(content=content, media_type="application/xml")  # custom response
