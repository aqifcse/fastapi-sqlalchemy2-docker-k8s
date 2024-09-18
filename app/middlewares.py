from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request


class CustomHeaderMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        response.headers['X-Custom-Header'] = 'Custom value'
        return response
