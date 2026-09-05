from hashlib import sha256
import os

from fastapi import Cookie, FastAPI, UploadFile
#from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel

from database import Database

app = FastAPI()
"""
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
"""

app.frontend("/", directory="../frontend", fallback="404.html")

db = Database()
def hash_password(password : str):
    return sha256(password.encode()).hexdigest()
hashed_password : str = hash_password(str(os.getenv("PASSWORD")))

if not os.path.isdir("img"):
    os.mkdir("img")

class Cookies(BaseModel):
    admin : str | None = None

def validate_cookie(cookie : Cookies) -> bool:
    return (cookie.admin == hashed_password)

@app.get("/api")
def index():
    return "Hello!"

class GuestbookEntry(BaseModel):
    username : str
    message : str

@app.post("/api/guestbook")
def guestbook_post(entry : GuestbookEntry):
    if entry.username != "" and entry.message != "":
        if db.guestbook.post(entry.username, entry.message)
            return JSONResponse("Posted!", 200);
        else:
            return JSONResponse("Error!", 500)
    return JSONResponse("Entries can't be empty!", 400)

@app.get("/api/guestbook")
def guestbook_get():
    return db.guestbook.get()

@app.delete("/api/guestbook/{id}")
def guestbook_delete(id : int, cookie : Cookies = Cookie()):
    if not validate_cookie(cookie):
        return JSONResponse("Unauthorized!", 401)
    else:
        if db.guestbook.delete(id):
            return JSONResponse("Deleted!", 200)
        else:
            return JSONResponse("Entry not found!", 404)

class BlogEntry(BaseModel):
    title : str
    content : str

@app.post("/api/blog")
def blog_post(entry : BlogEntry, cookie : Cookies = Cookie()):
    if not validate_cookie(cookie):
        return JSONResponse("Unauthorized!", 401)
    else:
        if db.blog.post(entry.title, entry.content):
            return JSONResponse("Posted!", 200)
        else:
            return JSONResponse("Error!", 500)

@app.get("/api/blog")
def blog_get():
    return db.blog.get()

@app.get("/api/blog/{id}")
def blog_get_by_id(id : int):
    data = db.blog.get_by_id(id)
    if len(data) == 0:
       return JSONResponse("Can't find blog with this id!", status_code=404)
    else:
        return data

@app.delete("/api/blog/{id}")
def blog_delete(id : int, cookie : Cookies = Cookie()):
    if not validate_cookie(cookie):
        return JSONResponse("Unauthorized!", 401)
    else:
        if db.blog.delete(id):
            return JSONResponse("Deleted!", 200)
        else:
            return JSONResponse("Entry not found!", 404)

@app.put("/api/blog/{id}")
def blog_update(id : int, entry : BlogEntry, cookie : Cookies = Cookie()):
    if not validate_cookie(cookie):
        return JSONResponse("Unauthorized!", 401)
    else:
        if db.blog.update(id, entry.title, entry.content):
            return JSONResponse("Updated!", 200)
        else:
            return JSONResponse("Entry not found!", 404)

@app.post("/api/projects")
def projects_post(entry : BlogEntry, cookie : Cookies = Cookie()):
    if not validate_cookie(cookie):
        return JSONResponse("Unauthorized!", 401)
    else:
        if db.projects.post(entry.title, entry.content):
            return JSONResponse("Posted!", 200)
        else:
            return JSONResponse("Error!", 500)

@app.get("/api/projects")
def projects_get():
    return db.projects.get()

@app.get("/api/projects/{id}")
def projects_get_by_id(id : int):
    data = db.projects.get_by_id(id)
    if len(data) == 0:
       return JSONResponse("Can't find project with this id!", status_code=404)
    else:
        return data

@app.delete("/api/projects/{id}")
def projects_delete(id : int, cookie : Cookies = Cookie()):
    if not validate_cookie(cookie):
        return JSONResponse("Unauthorized!", 401)
    else:
        if db.projects.delete(id):
            return JSONResponse("Deleted!", 200)
        else:
            return JSONResponse("Entry not found!", 404)

@app.put("/api/projects/{id}")
def projects_update(id : int, entry : BlogEntry, cookie : Cookies = Cookie()):
    if not validate_cookie(cookie):
        return JSONResponse("Unauthorized!", 401)
    else:
        if db.projects.update(id, entry.title, entry.content):
            return JSONResponse("Updated!", 200)
        else:
            return JSONResponse("Entry not found!", 404)

@app.get("/api/images/{id}")
def images_get_by_id(id : str):
    for filename in os.listdir("img"):
        if filename.split(".")[0] == str(id):
            return FileResponse(f"img/{filename}", 200)

    return JSONResponse("Image not found!", 404)

@app.get("/api/images")
def images_get():
    images = []
    for filename in os.listdir("img"):
        images.append(filename.split(".")[0])

    images.sort()
    images.reverse()
    return images

@app.post("/api/images")
async def images_post(file : UploadFile, cookie : Cookies = Cookie()):
    if not validate_cookie(cookie):
        return JSONResponse("Unauthorized!", 401)

    if not file.content_type in ["image/jpeg", "image/png", "image/gif"] :
        return JSONResponse("Wrong file type!", 415)

    filename = str(file.filename).split(".")
    extension = filename[len(filename)-1]
    new_id = 0
    if len(os.listdir("img")) > 0:
        ids = []
        for filename in os.listdir("img"):
            ids.append(int(filename.split(".")[0]))
            new_id = max(ids)+1
    filename = f"{new_id}.{extension}"

    with open(f"img/{filename}", "wb") as f:
        content = await file.read()
        f.write(content)

    return JSONResponse("Uploaded!", 200)

@app.delete("/api/images/{id}")
def images_delete(id : str, cookie : Cookies = Cookie()):
    if not validate_cookie(cookie):
        return JSONResponse("Unauthorized!", 401)

    for filename in os.listdir("img"):
        if filename.split(".")[0] == str(id):
            os.remove(f"img/{filename}")
            return JSONResponse("Deleted!", 200)

    return JSONResponse("Image not found!", 404)

class Login(BaseModel):
    password : str

@app.post("/api/login")
def login(login : Login):
    hash = hash_password(login.password)
    if hash == hashed_password:
        response = JSONResponse("ok", 200)
        response.set_cookie(key="admin", value=hash)
        return response
    return JSONResponse("Wrong password!", 401)

@app.get("/api/check-cookie")
def check_cookie(cookie : Cookies = Cookie()):
    if validate_cookie(cookie):
        return JSONResponse("Correct!", 200)
    return JSONResponse("Incorrect!", 401)
