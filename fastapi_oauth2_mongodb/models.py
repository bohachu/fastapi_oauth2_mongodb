from typing import Union

from pydantic import BaseModel

from fastapi_oauth2_mongodb.time import now


class User(BaseModel):
    username: str
    email: Union[str, None] = None
    full_name: Union[str, None] = None
    disabled: Union[bool, None] = None


class UserInDB(User):
    hashed_password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None


class RegisterData(BaseModel):
    username: str
    password: str
    email: str


class ActionResult(BaseModel):
    action: str
    username: str
    time: str
    success: bool
    message: str = ""


class RegisterResult(ActionResult):
    action: str = "RegisterResult"


class LoginResult(ActionResult):
    action: str = "LoginResult"
    token: str = None


class CurrentUserResult(ActionResult):
    action: str = "CurrentUserResult"
