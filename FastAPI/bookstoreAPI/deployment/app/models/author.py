# from models.book import Book
from typing import List

from pydantic import BaseModel


class Author(BaseModel):
    name: str
    books: List[str]
