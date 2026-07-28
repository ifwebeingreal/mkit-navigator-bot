from typing import Callable, Awaitable, Dict, Any

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery

import app.keyboards.inline as ikb

from config import config


class CheckSubscription(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        chat_member = await event.bot.get_chat_member(config.bot.channel_id, event.from_user.id)

        if chat_member.status == "left":
            await event.answer(
                """⚠️ Пифия пока тебя не видит.
Чтобы пройти тест, подпишись на наш канал — это твой ключ к системе.
После подписки нажми кнопку ещё раз 👇""",
                reply_markup=ikb.check_sub
            )
        else:
            return await handler(event, data)


class CheckSubscriptionCallback(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[CallbackQuery, Dict[str, Any]], Awaitable[Any]],
        event: CallbackQuery,
        data: Dict[str, Any]
    ) -> Any:
        chat_member = await event.bot.get_chat_member(config.bot.channel_id, event.from_user.id)

        if chat_member.status == "left":
            await event.message.delete()

            await event.message.answer(
                """⚠️ Пифия пока тебя не видит.
Чтобы пройти тест, подпишись на наш канал — это твой ключ к системе.
После подписки нажми кнопку ещё раз 👇""",
                reply_markup=ikb.check_sub
            )
        else:
            return await handler(event, data)
