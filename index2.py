from fastapi import FastAPI, Form, File, UploadFile, Header, Cookie, Request
from typing import Any, List, Optional

app = FastAPI()


@app.get("/")
async def home(user_agent: str = Header(...)) -> Any:
    return {"header": user_agent}


@app.get("/cookies")
async def get_cookie(user_agent: Optional[str] = Cookie(None)) -> Any:
    return {"user_agent": user_agent}


@app.get("/request")
async def request(request: Request) -> Any:
    return {"request_path": request.url.path}


@app.post("/users")
async def create_user(name: str = Form(...), age: int = Form(...)) -> Any:
    return {"name": name, "age": age}


@app.post("/files")
async def file_upload(file: bytes = File(...)) -> Any:
    return {"files": len(file)}


@app.post("/files2")
async def file_upload2(file: UploadFile = File(...)) -> Any:
    return {"file_name": file.filename, "content_type": file.content_type}


@app.post("/multiple_files")
async def multiple_file_uploads(files: List[UploadFile] = File(...)) -> Any:
    return [
        {
            "file_name": file.filename,
            "content_type": file.content_type
        } for file in files
    ]
