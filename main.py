import sys
import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from aiogram_dialog import setup_dialogs

from aiogram.fsm.storage.base import DefaultKeyBuilder
from aiogram.fsm.storage.redis import RedisStorage
import redis.asyncio as aioredis

from app.filters.check_sub import CheckSubscription, CheckSubscriptionCallback
from app.filters.admin_filter import AdminProtect
from config import config

from app.handlers.user_message import user
from app.handlers.admin_message import admin
from app.handlers.request_message import request

from app.handlers.quiz_message.dialog import quiz_dialog, quiz

from app.database.models import create_db


async def main():
    print("Bot is starting...")

    redis = await aioredis.from_url(config.redis.redis_url)
    await create_db()

    bot = Bot(
        token=config.bot.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher(storage=RedisStorage(redis, DefaultKeyBuilder(with_destiny=True)))

    # dp.message.middleware(CheckSubscription())
    # dp.callback_query.middleware(CheckSubscriptionCallback())
    quiz.message.middleware(CheckSubscription())
    quiz.callback_query.middleware(CheckSubscriptionCallback())

    admin.message.middleware(AdminProtect())
    admin.callback_query.middleware(AdminProtect())

    dp.include_router(user)
    dp.include_router(request)
    dp.include_router(admin)

    dp.include_router(quiz_dialog)
    dp.include_router(quiz)

    setup_dialogs(dp)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot stopped!")
