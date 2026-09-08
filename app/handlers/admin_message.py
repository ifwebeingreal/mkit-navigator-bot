from aiogram import F, Router, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

import app.keyboards.builder as bkb
import app.keyboards.inline as ikb

from app.database.requests.user.select import (
    get_statistics,
    get_users,
    get_users_count,
    get_quiz_statistics,
)
from app.database.requests.admin.select import get_admins, get_admin
from app.database.requests.admin.delete import delete_admin
from app.database.requests.admin.add import set_admin

from app.states import AddAdmin, SendAll

admin = Router()


@admin.message(Command("admin"))
@admin.message(F.text == "Админ-панель")
async def admin_panel(message: Message):
    daily_users, monthly_users, total_users = await get_statistics()
    daily_quiz, monthly_quiz, total_quiz = await get_quiz_statistics()
    admins = await get_admins()

    for admin in admins:
        if admin.tg_id == message.from_user.id:

            response = (
                f"<b>🛠 Админ-панель МКИТ</b>\n\n"
                f"<b>👥 Пользователи:</b>\n"
                f"📊 Сегодня: <b>{daily_users}</b>\n"
                f"📅 За месяц: <b>{monthly_users}</b>\n"
                f"🌍 Всего: <b>{total_users}</b>\n\n"
                f"<b>🧠 Прохождения квиза:</b>\n"
                f"📊 Сегодня: <b>{daily_quiz}</b>\n"
                f"📅 За месяц: <b>{monthly_quiz}</b>\n"
                f"🏁 Всего: <b>{total_quiz}</b>\n\n"
                f"✨ <i>Система работает стабильно</i>"
            )

            await message.answer(text=response, reply_markup=ikb.admin_panel)
            return


@admin.callback_query(F.data == "admins")
async def all_admins(callback: CallbackQuery):
    await callback.message.edit_text(
        "<b>Текущие администраторы бота:</b>", reply_markup=await bkb.admins_cb()
    )


@admin.callback_query(F.data == "add_admin")
async def add_admin(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "<b>Введите Telegram ID администратора:</b>", reply_markup=ikb.admin_cancel
    )

    await state.set_state(AddAdmin.tg_id)


@admin.message(AddAdmin.tg_id)
async def add_admin(message: Message, state: FSMContext):
    if message.text and message.text.isdigit():
        await set_admin(int(message.text))

        await message.answer(
            "<b>Администратор успешно добавлен!</b>", reply_markup=await bkb.admins_cb()
        )

        await state.clear()

    else:
        await message.answer(
            "<b>Введите корректный Telegram ID!</b>", reply_markup=ikb.admin_cancel
        )


@admin.callback_query(F.data.startswith("admin_"))
async def admin_info_panel(callback: CallbackQuery):
    admin_id = int(callback.data.split("_")[1])
    admin_info = await get_admin(admin_id)

    await callback.message.edit_text(
        f"<b>Панель управления администратором №{admin_info.id}:</b>\n\n"
        f"<b>Telegram ID:</b> {admin_info.tg_id}\n\n"
        f"<b><i>Выберите действие:</i></b>",
        reply_markup=await bkb.edit_admin(admin_id),
    )


@admin.callback_query(F.data.startswith("deleteadmin_"))
async def remove_admin(callback: CallbackQuery):
    admin_id = int(callback.data.split("_")[1])
    await delete_admin(admin_id)

    await callback.message.edit_text(
        "<b>Администратор успешно удален!</b>", reply_markup=await bkb.admins_cb()
    )


@admin.callback_query(F.data == "sender")
async def sender(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "Отправьте сообщение для рассылки:", reply_markup=ikb.admin_cancel
    )

    await state.set_state(SendAll.text)


@admin.message(SendAll.text)
async def send_all(message: Message, state: FSMContext, bot: Bot):
    users = await get_users()

    for user in users:
        try:
            await bot.copy_message(user.tg_id, message.chat.id, message.message_id)
        except Exception as e:
            if str(e) == "Forbidden: bot was blocked by the user":
                continue
            else:
                continue

    count = await get_users_count()

    await message.answer(
        f"Сообщение было отправлено {count} пользователям!",
        reply_markup=ikb.admin_panel,
    )
    await state.clear()


@admin.callback_query(F.data == "back")
async def back(callback: CallbackQuery, state: FSMContext):
    daily_users, monthly_users, total_users = await get_statistics()
    daily_quiz, monthly_quiz, total_quiz = await get_quiz_statistics()
    admins = await get_admins()

    for admin in admins:
        if admin.tg_id == callback.from_user.id:
            response = (
                f"<b>🛠 Админ-панель МКИТ</b>\n\n"
                f"<b>👥 Пользователи:</b>\n"
                f"📊 Сегодня: <b>{daily_users}</b>\n"
                f"📅 За месяц: <b>{monthly_users}</b>\n"
                f"🌍 Всего: <b>{total_users}</b>\n\n"
                f"<b>🧠 Прохождения квиза:</b>\n"
                f"📊 Сегодня: <b>{daily_quiz}</b>\n"
                f"📅 За месяц: <b>{monthly_quiz}</b>\n"
                f"🏁 Всего: <b>{total_quiz}</b>\n\n"
                f"✨ <i>Система работает стабильно</i>"
            )

            await callback.message.edit_text(
                text=response, reply_markup=ikb.admin_panel
            )

            await state.clear()
            return
