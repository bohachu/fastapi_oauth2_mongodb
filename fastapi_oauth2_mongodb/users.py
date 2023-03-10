from datetime import timedelta

from jose import jwt, JWTError
from pymongo import errors
from starlette import status
from starlette.exceptions import HTTPException

from fastapi_oauth2_mongodb.auth_token import ACCESS_TOKEN_EXPIRE_MINUTES, \
    create_access_token, SECRET_KEY, ALGORITHM
from fastapi_oauth2_mongodb.database import users_collection
from fastapi_oauth2_mongodb.hash import pwd_context
from fastapi_oauth2_mongodb.models import RegisterData, RegisterResult, LoginResult, CurrentUserResult
from fastapi_oauth2_mongodb.time import now


async def current_user(token: str) -> CurrentUserResult:
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
    except JWTError:
        raise credentials_exception
    user = await users_collection.find_one({"username": username})
    if user is None:
        raise credentials_exception
    return CurrentUserResult(username=user["username"], email=user["email"])


async def register(data: RegisterData) -> RegisterResult:
    existing_user = await users_collection.find_one({"username": data.username})
    if existing_user:
        return RegisterResult(action="register", username=data.username, time=now(),
                              success=False, message="Registration failed, user existed.")
    try:
        await users_collection.insert_one(
            {"username": data.username, "hashed_password": pwd_context.hash(data.password), "email": data.email})
        return RegisterResult(action="register", username=data.username, time=now(),
                              success=True, message="Registration success.")
    except errors.PyMongoError as e:
        return RegisterResult(action="register", username=data.username, time=now(),
                              success=False, message=f"Registration failed, exception: {e}")


async def login(username: str, password: str) -> LoginResult:
    existing_user = await users_collection.find_one({"username": username})
    if not existing_user or not pwd_context.verify(password, existing_user["hashed_password"]):
        return LoginResult(username=username, time=now(), success=False, message="Login failed.")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": existing_user["username"]}, expires_delta=access_token_expires)
    return LoginResult(username=existing_user["username"], time=now(), success=True, message="Login success.",
                       token=access_token)
