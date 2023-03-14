from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from fastapi_oauth2_mongodb.models import User, RegisterResult
from fastapi_oauth2_mongodb.users import register, login

router = APIRouter()


@router.post("/api/users/v1/register", status_code=status.HTTP_200_OK, response_model=RegisterResult)
async def api_users_v1_register(user: User):
    return await register(user)


@router.post("/api/users/v1/login", status_code=status.HTTP_200_OK, response_model=dict)
async def api_users_v1_login(form_data: OAuth2PasswordRequestForm = Depends()):
    # form_data.username value is email
    return await login(form_data.username, form_data.password)
