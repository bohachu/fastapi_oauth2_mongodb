from typing import Union

from pydantic import BaseModel


class User(BaseModel):
    email: Union[str, None] = None
    password: Union[str, None] = None
    hashed_password: Union[str, None] = None


class APIKey(BaseModel):
    email: str
    api_key: str


class Token(BaseModel):
    access_token: str
    token_type: str
    email: Union[str, None] = None


class Trial(BaseModel):
    email: str


class ActionResult(BaseModel):
    action: str
    email: str
    time: str
    success: bool
    message: str = ""


class RegisterResult(ActionResult):
    action: str = "RegisterResult"


class CreateTrialUserResult(ActionResult):
    action: str = "CreateTrialUserResult"


class LoginResult(ActionResult):
    action: str = "LoginResult"
    token: str = None


class CreateApiKeyResult(ActionResult):
    action: str = "CreateApiKeyResult"
    api_key: str = None
