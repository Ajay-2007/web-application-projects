import asyncio
from databases import Database

import sys

sys.path.append("/home/ajay/upwork/github/web-application-projects/FastAPI/bookstoreAPI/")
from utils.const import DB_URL


async def connect_db():
    db = Database(DB_URL)
    await db.connect()
    return db


async def disconnect_db(db):
    await db.disconnect()


async def execute(query, is_many, values=None):
    db = await connect_db()

    if is_many:
        await db.execute_many(query=query, values=values)
    else:
        await db.execute(query=query, values=values)

    await disconnect_db(db)


async def fetch(query, is_one, values=None):
    db = await connect_db()

    if is_one:
        result = await db.fetch_one(query=query, values=values)
        out = dict(result)
    else:
        result = await db.fetch_all(query=query, values=values)
        out = []
        for row in result:
            out.append(dict(row))

    await disconnect_db(db)

    # print(out)
    return out

# query = "insert into books values(:custom, :name, :author, :year)"
# #
# values = [dict(custom="isbn2", name="book2", author="author2", year=2019),
#           dict(custom="isbn3", name="book3", author="author3", year=2018),
#           dict(custom="isbn4", name="book4", author="author4", year=2020)]
# values = dict(isbn="isbn1", name="book1", author="author1", year=2019)

# query = "select * from books where isbn=:isbn"
# values = dict(isbn="isbn2")
# query = "select * from books"
# loop = asyncio.get_event_loop()
# # loop.run_until_complete(execute(query=query, is_many=True, values=values))
# loop.run_until_complete(fetch(query, False))
