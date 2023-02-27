import json
from typing import Callable

from bson import json_util
from starlette.requests import Request
from starlette.responses import StreamingResponse, JSONResponse
from starlette.types import Message

from fastapi_oauth2_mongodb.database import logs_collection
from fastapi_oauth2_mongodb.time import now


async def logs_middleware(request: Request, call_next: Callable):
    await log_request(request)
    return await log_response(call_next, request)


async def log_response(call_next, request):
    response: StreamingResponse = await call_next(request)
    if "application/json" in response.headers.get("content-type", ""):
        json_string = b''
        async for chunk in response.body_iterator:
            json_string += chunk
        dic = json.loads(json_string.decode(response.charset))
        dic.update({"action": "HttpResponse"})
        await logs_collection.insert_one(json.loads(json_util.dumps(dic)))
        return JSONResponse(dic)
    else:
        return response


async def log_request(request):
    async def restore_request_body(request: Request, body: bytes):
        async def receive() -> Message:
            return {'type': 'http.request', 'body': body}

        request._receive = receive

    request_dict = {
        "action": "HttpRequest",
        "time": now(),
        "method": request.method,
        "url": str(request.url),
        "headers": dict(request.headers),
        "query_params": dict(request.query_params),
        "path_params": request.path_params,
        "body": await request.body(),
        "client_host": request.client.host,
        "client_port": request.client.port
    }
    await logs_collection.insert_one(json.loads(json_util.dumps(request_dict)))
    await restore_request_body(request, request_dict["body"])
