from datetime import datetime
from typing import Union

from pydantic import BaseModel

from database import db


class MongoDBModel(BaseModel):
    created_at: Union[datetime, None] = None
    updated_at: Union[datetime, None] = None

    async def save(self):
        self.created_at = datetime.utcnow()
        self.updated_at = self.created_at
        document = self.dict()
        await self.collection().insert_one(document)

    def collection(self):
        return db[self.__class__.__name__.lower()]


class User(MongoDBModel):
    email: Union[str, None] = None  # index
    password: Union[str, None] = None
    hashed_password: Union[str, None] = None


class APIKey(MongoDBModel):
    email: str  # index
    api_key: str


class Token(BaseModel):
    access_token: str
    token_type: str
    email: Union[str, None] = None


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
