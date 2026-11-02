import asyncio
import random

from starlette.middleware.base import BaseHTTPMiddleware


class SimulatedLatencyMiddleware(BaseHTTPMiddleware):
    """Adds a random delay to GET requests so local dev behaves more like a real network."""

    def __init__(self, app, max_ms: int):
        super().__init__(app)
        self.max_ms = max_ms

    async def dispatch(self, request, call_next):
        if self.max_ms > 0 and request.method == "GET":
            await asyncio.sleep(random.uniform(0, self.max_ms) / 1000)
        return await call_next(request)
