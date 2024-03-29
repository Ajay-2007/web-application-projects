from fastapi import FastAPI, Depends, HTTPException

from routes.v1 import app_v1
from routes.v2 import app_v2
from starlette.requests import Request
from starlette.responses import Response
from starlette.status import HTTP_401_UNAUTHORIZED
from utils.security import check_jwt_token
import time
from datetime import datetime
from fastapi.security import OAuth2PasswordRequestForm
from utils.security import authenticate_user, create_jwt_token
from models.jwt_user import JWTUser
from utils.const import TOKEN_DESCRIPTION, TOKEN_SUMMARY, REDIS_URL, TESTING, IS_LOAD_TEST, IS_PRODUCTION, \
    REDIS_URL_PRODUCTION
from utils.db_object import db
import utils.redis_object as ro
import aioredis
from utils.redis_object import check_test_redis
import pickle

app = FastAPI(title="Bookstore API Documentation", description="It is an API that is used for bookstore",
              version="1.0.0")

app.include_router(app_v1, prefix='/v1', dependencies=[Depends(check_jwt_token), Depends(check_test_redis)])
app.include_router(app_v1, prefix='/v2', dependencies=[Depends(check_jwt_token), Depends(check_test_redis)])


@app.on_event("startup")
async def connect_db():
    if not TESTING:
        await db.connect()
        if IS_PRODUCTION:
            ro.redis = await aioredis.create_redis_pool(REDIS_URL_PRODUCTION)
        else:
            ro.redis = await aioredis.create_redis_pool(REDIS_URL)


@app.on_event("shutdown")
async def disconnect_db():
    if not TESTING:
        await db.disconnect()
        ro.redis.close()
        await ro.redis.wait_closed()


@app.get("/")
async def health_check():
    return {"result": "OK"}


@app.post("/token", description=TOKEN_DESCRIPTION, summary=TOKEN_SUMMARY)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    redis_key = f"token:{form_data.username},{form_data.password}"
    user = await ro.redis.get(redis_key)

    if not user:

        jwt_user_dict = {
            "username": form_data.username,
            "password": form_data.password
        }
        jwt_user = JWTUser(**jwt_user_dict)
        user = await authenticate_user(jwt_user)

        await ro.redis.set(redis_key, pickle.dumps(user))
        if user is None:
            raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)
    else:
        user = pickle.loads(user)

    jwt_token = create_jwt_token(user)
    return {"access_token": jwt_token}


@app.middleware("http")
async def middleware(request: Request, call_next):
    start_time = datetime.utcnow()
    # modify request

    # if not str(request.url).__contains__("/token"):

    # if not any(word in str(request.url) for word in ["/token", "/docs", "/openapi.json"]):
    #     try:
    #         jwt_token = request.headers['Authorization'].split("Bearer ")[1]
    #         is_valid = check_jwt_token(token=jwt_token)
    #     except Exception as ex:
    #         is_valid = False
    #     if not is_valid:
    #         return Response("Unauthorized", status_code=HTTP_401_UNAUTHORIZED)

    response = await call_next(request)
    # modify response
    execution_time = (datetime.utcnow() - start_time).microseconds
    response.headers["x-execution-time"] = str(execution_time) + "ms"
    return response
