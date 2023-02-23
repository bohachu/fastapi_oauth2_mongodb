from datetime import datetime

from fastapi import APIRouter, HTTPException

from database import collection
from models import RegisterData, RegisterResult

router = APIRouter()


@router.post("/api/register", response_model=RegisterResult)
async def register(data: RegisterData):
    existing_user = collection.find_one({"username": data.username})
    if existing_user:
        raise HTTPException(status_code=409, detail="Username already exists")
    result = collection.insert_one(data.dict())
    result_data = RegisterResult(
        username=data.username,
        time=datetime.utcnow().isoformat(),
        success=True,
        message="Registration success."
    )
    return result_data
