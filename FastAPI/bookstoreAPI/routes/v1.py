from fastapi import FastAPI, Body, Header, File, Depends, HTTPException, APIRouter
from starlette.responses import Response
from starlette.status import HTTP_201_CREATED, HTTP_401_UNAUTHORIZED

from models.author import Author
from models.book import Book
from models.user import User


app_v1 = APIRouter()


@app_v1.post("/user", status_code=HTTP_201_CREATED, tags=["User"])
async def post_user(user: User, x_custom: str = Header("default")):
    return {
        "request body": user,
        "request custom header": x_custom
    }


@app_v1.get("/user")
async def get_user_validation(password: str):
    return {
        "parameter": password
    }


@app_v1.get("/book/{isbn}", response_model=Book, response_model_include=["name", "year"], tags=["Book"])
async def get_book_with_isbn(isbn: str):
    author_dict = {
        "name": "author1",
        "book": ["book1", "book2"]
    }

    author1 = Author(**author_dict)
    book_dict = {
        "isbn": "isbn1",
        "name": "book1",
        "year": 2019,
        "author": author1
    }
    book1 = Book(**book_dict)

    return book1


@app_v1.get("/author/{id}/book", tags=["Book"])
async def get_authors_books(idk: int, category: str, order: str = "asc", ):
    return {
        "query changable parameter": order + category + str(idk)
    }


@app_v1.patch("/author/name")
async def patch_author_name(name: str = Body(..., embed=True)):
    return {
        "name in body": name
    }


@app_v1.post("/user/author")
async def post_user_and_author(user: User, author: Author, bookstore_name: str = Body(..., embed=True)):
    return {
        "user": user,
        "author": author,
        "bookstore_name": bookstore_name
    }


@app_v1.post("/user/photo")
async def upload_user_photo(response: Response, profile_photo: bytes = File(...)):
    response.headers["x-file-size"] = str(len(profile_photo))
    response.set_cookie(key="cookie-a pi", value="test")
    return {
        "file size": len(profile_photo)
    }

