import os

import uvicorn
from fastapi import FastAPI
from starlette.responses import RedirectResponse

from fastapi_oauth2_mongodb.router_users import router

app = FastAPI()
app.include_router(router)


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
