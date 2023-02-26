from datetime import datetime
from fastapi import Depends, APIRouter, HTTPException, status
from database import collection
from models import RegisterData, RegisterResult, Token
from hash import pwd_context
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from typing import Union
from jose import JWTError, jwt
import secrets

router = APIRouter()


@router.post("/api/account/v1/register", response_model=RegisterResult)
async def register(data: RegisterData):
    existing_user = collection.find_one({"username": data.username})
    if existing_user:
        raise HTTPException(status_code=409, detail="Username already exists")
    dic = {"username": data.username, "hashed_password": pwd_context.hash(data.password), "email": data.email}
    result = collection.insert_one(dic)
    result_data = RegisterResult(
        username=data.username,
        time=datetime.utcnow().isoformat(),
        success=True,
        message="Registration success."
    )
    return result_data


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


@router.post("/api/account/v1/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    existing_user = collection.find_one({"username": form_data.username})
    if not pwd_context.verify(form_data.password, existing_user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": existing_user["username"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
