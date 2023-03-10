from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from fastapi_oauth2_mongodb.models import RegisterData, RegisterResult
from fastapi_oauth2_mongodb.users import register, login, current_user

router = APIRouter()


@router.post("/api/users/v1/register", status_code=status.HTTP_200_OK, response_model=RegisterResult)
async def api_users_v1_register(register_data: RegisterData):
    return await register(register_data)


@router.post("/api/users/v1/login", status_code=status.HTTP_200_OK, response_model=dict)
async def api_users_v1_login(form_data: OAuth2PasswordRequestForm = Depends()):
    return await login(form_data.username, form_data.password)


@router.get("/api/users/v1/current_user", status_code=status.HTTP_200_OK, response_model=dict)
async def api_users_v1_current_user(token: str):
    return await current_user(token)
