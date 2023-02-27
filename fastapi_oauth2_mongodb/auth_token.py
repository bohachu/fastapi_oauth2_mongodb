import secrets
from datetime import timedelta, datetime
from typing import Union

from fastapi.security import OAuth2PasswordBearer
from jose import jwt

ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24
SECRET_KEY = secrets.token_urlsafe(32)
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
