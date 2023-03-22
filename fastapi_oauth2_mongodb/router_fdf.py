from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import requests
import os
import subprocess
import shutil
import uuid

router = APIRouter()


class CodeRequest(BaseModel):
    requirements_txt: str
    main_py: str


@router.post("/api/fdf/v1/run_code")
async def run_code(code_request: CodeRequest, x_falra_key: str):
    # 產生隨機 uuid4 的 folder
    folder_name = str(uuid.uuid4())
    os.makedirs(folder_name, exist_ok=True)

    # 將 requirements_txt 和 main_py 存到 uuid4 亂數的 folder
    with open(os.path.join(folder_name, 'requirements.txt'), 'w') as f:
        f.write(code_request.requirements_txt)
    with open(os.path.join(folder_name, 'main.py'), 'w') as f:
        f.write(code_request.main_py)

    # 切換到 uuid4 亂數的 folder
    os.chdir(folder_name)

    # 用 shell 命令的方式安裝 requirements.txt 裡面的套件
    subprocess.run(['pip', 'install', '-r', 'requirements.txt'], check=True)

    # 用 shell 命令的方式執行 main.py，並取得 stdout
    result = subprocess.run(['python', 'main.py'], capture_output=True, text=True)

    # 將執行結果回傳給呼叫方
    return result.stdout
