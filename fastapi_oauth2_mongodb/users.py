import argparse
import asyncio
from datetime import timedelta

from pymongo import errors

from fastapi_oauth2_mongodb.auth_token import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token
from fastapi_oauth2_mongodb.hash import pwd_context
from fastapi_oauth2_mongodb.models import User, RegisterResult, LoginResult, CreateTrialUserResult
from fastapi_oauth2_mongodb.time import now


async def register(user: User) -> RegisterResult:
    existing_user = await user.collection().find_one({"email": user.email})
    if existing_user:
        return RegisterResult(email=user.email, time=now(),
                              success=False, message="Registration failed, user already exists.")
    try:
        user.hashed_password = pwd_context.hash(user.password)
        user.password = ''
        await user.save()
        return RegisterResult(email=user.email, time=now(),
                              success=True, message="Registration successful.")
    except errors.PyMongoError as e:
        return RegisterResult(email=user.email, time=now(),
                              success=False, message=f"Registration failed, exception: {e}")


async def login(user: User) -> LoginResult:
    existing_user = await user.collection().find_one({"email": user.email})
    if not existing_user or not pwd_context.verify(user.password, existing_user["hashed_password"]):
        return LoginResult(email=user.email, time=now(), success=False, message="Login failed.")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": existing_user["email"]}, expires_delta=access_token_expires)
    return LoginResult(email=existing_user["email"], time=now(), success=True, message="Login success.",
                       token=access_token)


async def create_trial_user(user: User) -> CreateTrialUserResult:
    existing_user = await user.collection().find_one({"email": user.email})
    if existing_user:
        return CreateTrialUserResult(email=user.email, time=now(),
                                     success=False, message="Create trial user failed, user existed.")
    try:
        await user.save()
        return CreateTrialUserResult(email=user.email, time=now(),
                                     success=True, message="Create trial user success.")
    except errors.PyMongoError as e:
        return CreateTrialUserResult(email=user.email, time=now(),
                                     success=False, message=f"Create trial user failed, exception: {e}")


async def main():
    parser = argparse.ArgumentParser(description="FastAPI OAuth2 MongoDB CLI")
    subparsers = parser.add_subparsers(dest="command")

    register_parser = subparsers.add_parser("register", help="Register a new user")
    register_parser.add_argument("--email", required=True, help="Email")
    register_parser.add_argument("--password", required=True, help="Password")

    login_parser = subparsers.add_parser("login", help="Login with an existing user")
    login_parser.add_argument("--email", required=True, help="Email")
    login_parser.add_argument("--password", required=True, help="Password")

    create_trial_user_parser = subparsers.add_parser("create_trial_user", help="Create trial user")
    create_trial_user_parser.add_argument("--email", required=True, help="Email")

    args, unknown = parser.parse_known_args()

    if not args.command:
        parser.print_help()
        return

    if args.command == "register":
        result = await register(User(email=args.email, password=args.password))
        print(result)
    elif args.command == "login":
        result = await login(User(email=args.email, password=args.password))
        print(result)
    elif args.command == "create_trial_user":
        result = await create_trial_user(User(email=args.email))
        print(result)


if __name__ == "__main__":
    asyncio.run(main())
