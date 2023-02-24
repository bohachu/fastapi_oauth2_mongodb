from datetime import datetime

from fastapi import APIRouter, HTTPException

from database import collection
from models import RegisterData, RegisterResult
from hash import pwd_context

router = APIRouter()


@router.post("/api/register", response_model=RegisterResult)
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
