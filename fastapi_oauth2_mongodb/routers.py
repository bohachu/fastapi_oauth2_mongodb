# 設置 MongoDB 連接
from datetime import datetime

from fastapi import APIRouter, HTTPException

from database import collection
from models import RegisterData, RegisterResult

router = APIRouter()


@router.post("/api/register", response_model=RegisterResult)
async def register(data: RegisterData):
    # 檢查用戶名是否已存在
    existing_user = collection.find_one({"username": data.username})
    if existing_user:
        raise HTTPException(status_code=409, detail="Username already exists")
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

# @router.post("/api/register", response_model=RegisterResult)
# async def register(data: RegisterData):
#     # 在 MongoDB 中插入用戶數據
#     result = collection.insert_one(data.dict())
#     # 構建輸出數據
#     result_data = RegisterResult(
#         username=data.username,
#         time=datetime.utcnow().isoformat(),
#         success=True,
#         message="Registration success."
#     )
#     return result_data
