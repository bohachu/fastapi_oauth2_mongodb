# 設置 MongoDB 連接
from datetime import datetime

from fastapi import APIRouter

from database import collection
from models import RegisterData, RegisterResult

router = APIRouter()


@router.post("/api/register", response_model=RegisterResult)
async def register(data: RegisterData):
    # 在 MongoDB 中插入用戶數據
    result = collection.insert_one(data.dict())
    # 構建輸出數據
    result_data = RegisterResult(
        username=data.username,
        time=datetime.utcnow().isoformat(),
        success=True,
        message="Registration success."
    )
    return result_data
