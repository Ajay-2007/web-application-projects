from fastapi import FastAPI, Body, Header, File, Depends, HTTPException, APIRouter
from starlette.responses import Response
from starlette.status import HTTP_201_CREATED, HTTP_401_UNAUTHORIZED

from models.author import Author
from models.book import Book
from models.user import User
from utils.helper_functions import upload_image_to_server
from utils.db_functions import (db_insert_personal, db_check_personel,
                                db_get_book_with_isbn, db_get_author,
                                db_get_author_from_id, db_patch_author_name)
import utils.redis_object as ro
import pickle

app_v1 = APIRouter()


@app_v1.post("/user", status_code=HTTP_201_CREATED, tags=["User"])
async def post_user(user: User):
    await db_insert_personal(user)
    return {
        "result": "personal is created"
    }


@app_v1.post("/login")
async def get_user_validation(username: str = Body(...), password: str = Body(...)):
    redis_key = f"{username},{password}"
    result = await ro.redis.get(redis_key)

    # Redis has the data
    if result:
        if result == "true":
            return {"is_valid (redis)": True}
        else:
            return {"is_valid (redis)": False}

    # Redis does not have the data
    else:
        result = await db_check_personel(username, password)
        await ro.redis.set(redis_key, str(result), expire=10)

    return {"is_valid (db)": result}


@app_v1.get("/book/{isbn}", response_model=Book, response_model_include=["name", "year"], tags=["Book"])
async def get_book_with_isbn(isbn: str):
    result = await ro.redis.get(isbn)

    if result:
        result_book = pickle.loads(result)
        return result_book
    else:
        book = await db_get_book_with_isbn(isbn)
        author = await db_get_author(book["author"])
        author_obj = Author(**author)
        book["author"] = author_obj
        result_book = Book(**book)

        await ro.redis.set(isbn, pickle.dumps(result_book))

        return result_book


@app_v1.get("/author/{id}/book", tags=["Book"])
async def get_authors_books(id: int, order: str = "asc"):
    author = await db_get_author_from_id(id)
    if author is not None:
        books = author["books"]
        if order == "asc":
            books = sorted(books)
        else:
            books = sorted(books, reverse=True)

        return {"books": books}
    else:
        return {"No author with corresponding id!"}


@app_v1.patch("/author/{id}/name")
async def patch_author_name(id: int, name: str = Body(..., embed=True)):
    await db_patch_author_name(id, name)
    return {"result": "name is updated."}


@app_v1.post("/user/author")
async def post_user_and_author(user: User, author: Author, bookstore_name: str = Body(..., embed=True)):
    return {
        "user": user,
        "author": author,
        "bookstore_name": bookstore_name
    }


@app_v1.post("/user/photo")
async def upload_user_photo(response: Response, profile_photo: bytes = File(...)):
    await upload_image_to_server(profile_photo)
    return {"file size": len(profile_photo)}
