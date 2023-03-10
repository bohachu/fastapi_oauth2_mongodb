import argparse
import asyncio
import os
import textwrap
from typing import Optional, List, Dict

import openai
from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

load_dotenv()  # 讀取 .env 檔案

router = APIRouter()


class ChatMessage(BaseModel):
    messages: List[Dict[str, str]] = [{
        "role": "user",
        "content": """請給我完整的react typescript bootstrap示範程式碼"""}]
    model: Optional[str] = "gpt-3.5-turbo"


@router.post("/api/openai/v1/chat")
async def chat(chat_message: ChatMessage):
    try:
        openai.api_key = os.environ.get("OPENAI_API_KEY")  # 從 .env 讀取 API Key
        if openai.api_key is None:
            raise ValueError("Missing OpenAI API key in environment variable OPENAI_API_KEY.")
        completion = openai.ChatCompletion.create(
            model=chat_message.model,
            messages=chat_message.messages
        )
        return completion["choices"][0]["message"]["content"]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def main():
    parser = argparse.ArgumentParser(description='OpenAI chat client')
    parser.add_argument('--message', type=str, default='who are you?', help='The message to send to OpenAI')
    parser.add_argument('--model', type=str, default='gpt-3.5-turbo', help='The OpenAI engine to use')
    args = parser.parse_args()

    api_key = os.environ.get("OPENAI_API_KEY")
    if api_key is None:
        print("Missing OpenAI API key in environment variable OPENAI_API_KEY.")
        return

    chat_message = ChatMessage(messages=[{'role': 'user', 'content': args.message}], model=args.model)
    result = asyncio.run(chat(chat_message))
    print(textwrap.fill(result, width=30))


if __name__ == '__main__':
    main()
