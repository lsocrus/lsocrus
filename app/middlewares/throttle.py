# app/middlewares/throttle.py
import time
from typing import Any, Callable, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery

class Throttle(BaseMiddleware):
    def __init__(self, rate: float = 1.5):
        self.rate = rate
        self.last: dict[int, float] = {}

    async def __call__(self, handler: Callable, event: Message | CallbackQuery,
                       data: dict) -> Any:
        uid = event.from_user.id if event.from_user else 0
        now = time.monotonic()
        if now - self.last.get(uid, 0) < self.rate:
            if isinstance(event, CallbackQuery):
                await event.answer("⏳ Не так быстро", show_alert=False)
            return
        self.last[uid] = now
        return await handler(event, data)