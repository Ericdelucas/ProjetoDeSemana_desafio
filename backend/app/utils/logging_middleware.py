import time
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request


class RequestTimingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start = time.time()
        response = await call_next(request)
        elapsed_ms = int((time.time() - start) * 1000)
        response.headers["X-Response-Time-ms"] = str(elapsed_ms)
        print(f"[REQ] {request.method} {request.url.path} -> {response.status_code} ({elapsed_ms}ms)")
        return response