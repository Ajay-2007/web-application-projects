from fastapi import FastAPI

from routes.v1 import app_v1
from routes.v2 import app_v2
from starlette.requests import Request
from starlette.responses import Response
from starlette.status import HTTP_401_UNAUTHORIZED
from utils.security import check_jwt_token
import time
from datetime import datetime

app = FastAPI()

app.mount("/v1", app_v1)
app.mount("/v2", app_v2)


@app.middleware("http")
async def middleware(request: Request, call_next):
    start_time = datetime.utcnow()
    # modify request

    if not str(request.url).__contains__("/token"):
        try:
            jwt_token = request.headers['Authorization'].split("Bearer ")[1]
            is_valid = check_jwt_token(token=jwt_token)
        except Exception as ex:
            is_valid = False
        if not is_valid:
            return Response("Unauthorized", status_code=HTTP_401_UNAUTHORIZED)

    response = await call_next(request)
    # modify response
    execution_time = (datetime.utcnow() - start_time).microseconds
    response.headers["x-execution-time"] = str(execution_time) + "ms"
    return response
