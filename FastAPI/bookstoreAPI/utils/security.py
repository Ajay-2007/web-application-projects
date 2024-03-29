from passlib.context import CryptContext
import sys

sys.path.append("/home/ajay/upwork/github/web-application-projects/FastAPI/bookstoreAPI/")
from models.jwt_user import JWTUser
from datetime import datetime, timedelta
from utils.const import JWT_EXPIRATION_TIME_MINUTES, JWT_SECRET_KEY, JWT_ALGORITHM
import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
import time
from starlette.status import HTTP_401_UNAUTHORIZED
from utils.db_functions import db_check_jwt_token_user, db_check_jwt_username

oauth_schema = OAuth2PasswordBearer(tokenUrl="/token")
pwd_context = CryptContext(schemes=["bcrypt"])


def get_hashed_password(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception as ex:
        return False


# Authenticate username and password to give JWT token
async def authenticate_user(user: JWTUser):
    potential_users = await db_check_jwt_token_user(user)

    is_valid = False
    for db_user in potential_users:
        if verify_password(user.password, db_user["password"]):
            is_valid = True
    if is_valid:
        user.role = "admin"
        return user

    return None


# Create access JWT token
def create_jwt_token(user: JWTUser):
    expiration = datetime.utcnow() + timedelta(minutes=JWT_EXPIRATION_TIME_MINUTES)
    jwt_payload = {
        "sub": user.username,
        "role": user.role,
        "exp": expiration
    }
    jwt_token = jwt.encode(jwt_payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)

    return jwt_token


# Check whether JWT token is correct
async def check_jwt_token(token: str = Depends(oauth_schema)):
    try:
        jwt_payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=JWT_ALGORITHM)
        # print(jwt_payload)
        username = jwt_payload.get("sub")
        role = jwt_payload.get("role")
        expiration = jwt_payload.get("exp")
        if time.time() < expiration:
            is_valid = await db_check_jwt_username(username)
            if is_valid:
                return final_checks(role)
    except Exception as ex:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)

    raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)


# Last checking and returning the final result
def final_checks(role: str):
    if role == "admin":
        return True
    else:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)


# print(get_hashed_password("pass1"))
