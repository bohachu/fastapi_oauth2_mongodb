import argparse
import asyncio
import random
import string

from fastapi_oauth2_mongodb.database import api_keys_collection
from fastapi_oauth2_mongodb.models import APIKey, CreateApiKeyResult
from fastapi_oauth2_mongodb.time import now


def generate_api_key(length=32):
    chars = string.ascii_letters + string.digits
    api_key = ''.join(random.choice(chars) for _ in range(length))
    return 'rk-' + api_key


async def create_api_key(email):
    print("create_api_key,email", email)
    api_key = generate_api_key()
    api_key_obj = APIKey(email=email, api_key=api_key)
    await api_keys_collection.insert_one(api_key_obj.dict())
    return CreateApiKeyResult(email=email, time=now(), success=True, message="Create API key success.",
                              api_key=api_key)


async def main():
    parser = argparse.ArgumentParser(description='Generate and store an API key.')
    parser.add_argument('email', type=str, help='Email address of the API key owner.')
    args = parser.parse_args()
    print(await create_api_key(email=args.email))


if __name__ == "__main__":
    asyncio.run(main())
