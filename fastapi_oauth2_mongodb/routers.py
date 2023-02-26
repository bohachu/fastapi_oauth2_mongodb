from datetime import datetime

from fastapi import APIRouter, HTTPException

from database import collection
from fastapi_oauth2_mongodb import create_access_token
from fastapi_oauth2_mongodb.database import collection
from fastapi_oauth2_mongodb.fastapi_oauth2_mongodb import app, pwd_context, ACCESS_TOKEN_EXPIRE_MINUTES
from fastapi_oauth2_mongodb.models import Token
from models import RegisterData, RegisterResult
from hash import pwd_context

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


@app.post("/api/account/v1/login", response_model=Token)
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
