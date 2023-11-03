import asyncio
import logging

from app.config import settings
from app.handlers import notify
from app.bot import bot, dp


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )

    dp.include_routers(
        notify.router,
    )

    # Подгрузка списка редакторов
    editors = settings.EDITORS
    editors_ids = set(editors)

    chats = settings.CHATS
    chats_ids = set(chats)

    await dp.start_polling(bot, editors=editors_ids, chats=chats_ids)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
