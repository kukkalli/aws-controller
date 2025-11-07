from __future__ import annotations

import time
from typing import Callable, Dict, Tuple

from starlette.types import ASGIApp, Receive, Scope, Send
from starlette.responses import JSONResponse

# Simple in-memory token bucket per IP (dev only; use Redis for production).
class RateLimitMiddleware:
    def __init__(self, app: ASGIApp, requests_per_minute: int = 60) -> None:
        self.app = app
        self.limit = max(1, requests_per_minute)
        self._buckets: Dict[str, Tuple[int, float]] = {}

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope['type'] != 'http':
            await self.app(scope, receive, send)
            return

        client_ip = "unknown"
        client = scope.get("client")
        if client:
            client_ip = client[0]

        now = time.time()
        tokens, reset = self._buckets.get(client_ip, (self.limit, now + 60))
        if now > reset:
            tokens, reset = self.limit, now + 60

        if tokens <= 0:
            retry_after = max(1, int(reset - now))
            response = JSONResponse(
                {"detail": "Rate limit exceeded."},
                status_code=429,
                headers={
                    "Retry-After": str(retry_after),
                    "X-RateLimit-Limit": str(self.limit),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(int(reset)),
                },
            )
            await response(scope, receive, send)
            return

        self._buckets[client_ip] = (tokens - 1, reset)

        async def send_wrapper(message):
            if message["type"] == "http.response.start":
                headers = message.setdefault("headers", [])
                def add(name: str, value: str) -> None:
                    headers.append((name.encode('latin-1'), value.encode('latin-1')))
                remaining = max(0, self._buckets[client_ip][0])
                add("X-RateLimit-Limit", str(self.limit))
                add("X-RateLimit-Remaining", str(remaining))
                add("X-RateLimit-Reset", str(int(reset)))
            await send(message)

        await self.app(scope, receive, send_wrapper)
