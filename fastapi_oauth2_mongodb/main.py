import os

import uvicorn
from fastapi import FastAPI, APIRouter
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse

from fastapi_oauth2_mongodb.logs_middleware import logs_middleware
from fastapi_oauth2_mongodb.logstuff import LogStuff
from fastapi_oauth2_mongodb.router_users import router_users

middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
        allow_credentials=True,
    ),
]
app = FastAPI(middleware=middleware)

# app.router.route_class = LogStuff
app.middleware("http")(logs_middleware)
# app.middleware("http")(LogsMiddleware)
# app.include_router(APIRouter(route_class=LogStuff))

app.include_router(router_users)


@app.get("/")
async def root():
    return RedirectResponse(url="/docs")


def start_fastapi():
    os.system(f"docker run -d -p 27017:27017 --name mongodb -v ~/mongodb:/data/db mongo")
    uvicorn.run(app, host="0.0.0.0", port=8000)


def main():
    start_fastapi()


if __name__ == "__main__":
    main()
