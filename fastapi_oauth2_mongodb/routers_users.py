import pymongo
import pytest
from fastapi import Depends, APIRouter, status, HTTPException
from passlib.context import CryptContext

from fastapi_oauth2_mongodb.database import collection
from fastapi_oauth2_mongodb.models import RegisterData, RegisterResult, TokenData, User
from fastapi_oauth2_mongodb.hash import pwd_context
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from datetime import datetime, timedelta
from typing import Union
from jose import jwt, JWTError
import secrets

router = APIRouter()


@router.post("/api/users/v1/register", status_code=status.HTTP_200_OK, response_model=RegisterResult)
async def register(data: RegisterData):
    try:
        existing_user = collection.find_one({"username": data.username})
        message = "Registration failed, user existed." if existing_user else "Registration success."
        success = not existing_user
        if not existing_user:
            collection.insert_one(
                {"username": data.username, "hashed_password": pwd_context.hash(data.password), "email": data.email})
    except pymongo.errors.PyMongoError as e:
        message = f"Registration failed, exception: {e}"
        success = False
    return {"action": "register", "username": data.username, "time": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
            "success": success, "message": message}


ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24
SECRET_KEY = secrets.token_urlsafe(32)
ALGORITHM = "HS256"


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@router.post("/api/users/v1/login", status_code=status.HTTP_200_OK, response_model=dict)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        existing_user = collection.find_one({"username": form_data.username})
        if not existing_user or not pwd_context.verify(form_data.password, existing_user["hashed_password"]):
            return {"action": "login", "username": form_data.username,
                    "time": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"), "success": False,
                    "message": "Login failed."}
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(data={"sub": existing_user["username"]}, expires_delta=access_token_expires)
        return {"action": "login", "username": existing_user["username"],
                "time": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"), "success": True, "message": "Login success.",
                "token": access_token}
    except pymongo.errors.PyMongoError as e:
        return {"action": "login", "username": form_data.username,
                "time": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"), "success": False,
                "message": f"Login failed, exception: {e}"}


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = collection.find_one({"username": username})
    return user
