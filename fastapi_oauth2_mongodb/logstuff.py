from typing import Callable

from fastapi.routing import APIRoute
from starlette.requests import Request
from starlette.responses import Response


class LogStuff(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            request_body = await request.body()
            print('request_body', request_body)
            response: Response = await original_route_handler(request)
            response_body = response.body
            print('response_body', response_body)
            return response

        return custom_route_handler
