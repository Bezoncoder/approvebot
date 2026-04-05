from typing import Any, Awaitable, Callable, Dict
from aiogram import BaseMiddleware
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import Message, TelegramObject
from get_data_settings.get_config import config


class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, storage: RedisStorage, limit: int = 5, timeout: int = 600):
        self.storage = storage
        self.limit = limit
        self.timeout = timeout

    async def __call__(self,
                       handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
                       event: Message,
                       data: Dict[str, Any],
                       ) -> Any:
        if event.chat.id == config.admin_id:
            return await handler(event, data)
        user = f"user{event.chat.id}"
        count = await self.storage.redis.incr(name=user)
        if count == 1:
            await self.storage.redis.expire(name=user, time=self.timeout)
        if count == self.limit:
            return await event.answer("Не надо спамить. Ждите, пожалуйста...")
        if count > self.limit:
            return
        return await handler(event, data)
