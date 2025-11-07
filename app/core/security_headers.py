from __future__ import annotations
from typing import Callable
from starlette.types import ASGIApp, Receive, Scope, Send

class SecurityHeadersMiddleware:
    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope['type'] != 'http':
            await self.app(scope, receive, send)
            return

        async def send_wrapper(message):
            if message['type'] == 'http.response.start':
                headers = message.setdefault('headers', [])
                def add(name: str, value: str) -> None:
                    headers.append((name.encode('latin-1'), value.encode('latin-1')))
                add('x-content-type-options', 'nosniff')
                add('x-frame-options', 'DENY')
                add('referrer-policy', 'no-referrer')
                add('x-xss-protection', '1; mode=block')
                add('content-security-policy', "default-src 'self'")
            await send(message)
        await self.app(scope, receive, send_wrapper)
