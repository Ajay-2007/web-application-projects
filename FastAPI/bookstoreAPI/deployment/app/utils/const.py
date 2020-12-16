import os

JWT_SECRET_KEY = "74bf95403555b0346f1e7084d08293ec9337a9fd99f66a725087b9c61671e9c4"
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_TIME_MINUTES = 60 * 24 * 5

TOKEN_DESCRIPTION = "It checks username and password if they are true, it returns JWT token to you"
TOKEN_SUMMARY = "It returns JWT token."

ISBN_DESCRIPTION = "It is unique identifier for book"

DB_HOST = "127.0.0.1"
DB_USER = "admin"
DB_PASSWORD = "admin"
DB_NAME = "bookstore"

DB_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

UPLOAD_PHOTO_APIKEY = "c7396189860f92ffd7367991511bd99a"

UPLOAD_PHOTO_URL = f"https://api.imgbb.com/1/upload?key={UPLOAD_PHOTO_APIKEY}"

REDIS_URL = "redis://127.0.0.1"
REDIS_URL_PRODUCTION = "redis://127.0.0.1"  # IP address of production environment
TESTING = False
IS_LOAD_TEST = False
IS_PRODUCTION = True # if os.environ["PRODUCTION"] == "true" else False
TEST_DB_HOST = "127.0.0.1"
TEST_DB_USER = "test"
TEST_DB_PASSWORD = "test"
TEST_DB_NAME = "postgres"
TEST_DB_URL = f"postgresql://{TEST_DB_USER}:{TEST_DB_PASSWORD}@{TEST_DB_HOST}/{TEST_DB_NAME}"

TEST_REDIS_URL = "redis://127.0.0.1"

DB_HOST_PRODUCTION = "127.0.0.1"  # IP address of product environment
DB_URL_PRODUCTION = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST_PRODUCTION}/{DB_NAME}"
