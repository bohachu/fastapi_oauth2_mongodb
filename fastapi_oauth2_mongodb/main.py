import os

import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse

from fastapi_oauth2_mongodb import router_users, router_trial, router_fdf
from init_index import create_db_indexes

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    await create_db_indexes()


origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8000",
    "*"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router_users.router)
app.include_router(router_trial.router)
app.include_router(router_fdf.router)


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
