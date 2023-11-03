import logging
from typing import Callable, Dict, Any, Awaitable

from aiogram.types import CallbackQuery
from aiogram import BaseMiddleware


class StoreMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[CallbackQuery, Dict[str, Any]], Awaitable[Any]],
            event: CallbackQuery,
            data: Dict[str, Any]
    ) -> Any:
        logging.info(f"StoreMiddleware: {data=}")
        data["message_to_send"] = "NONE"
        return await handler(event, data)
