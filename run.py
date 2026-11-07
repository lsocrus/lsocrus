# run.py
import asyncio, logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from app.config import cfg
from app.db import init_db
from app.handlers import setup_handlers
from app.middlewares.throttle import Throttle

async def main():
    logging.basicConfig(level=logging.INFO)
    if not cfg.token:
        raise SystemExit("BOT_TOKEN не задан (.env)")
    await init_db()
    bot = Bot(cfg.token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()
    dp.message.middleware(Throttle(cfg.throttle_rate))
    dp.callback_query.middleware(Throttle(cfg.throttle_rate))
    setup_handlers(dp)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())