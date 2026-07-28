from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.database.requests.admin.select import get_admins


async def admins_cb():
    kb = InlineKeyboardBuilder()

    kb.row(InlineKeyboardButton(text="➕ Добавить администратора", callback_data="add_admin"))

    admins = await get_admins()
    for admin in admins:
        kb.row(InlineKeyboardButton(text=f"{admin.tg_id}", callback_data=f"admin_{admin.id}"))

    kb.row(InlineKeyboardButton(text="🔙 Назад", callback_data="back"))

    return kb.as_markup()


async def edit_admin(id: int):
    kb = InlineKeyboardBuilder()

    kb.row(InlineKeyboardButton(text="❌ Удалить", callback_data=f"deleteadmin_{id}"))
    kb.row(InlineKeyboardButton(text="🔙 Назад", callback_data=f"admins"))

    return kb.as_markup()


async def result_panel(key: str):
    kb = InlineKeyboardBuilder()

    kb.row(InlineKeyboardButton(text="👉🏻 Запросить консультацию", callback_data=f"send_request_{key}", style="danger"))
    kb.row(InlineKeyboardButton(text="🔁 Пройти тест заново", callback_data=f"start_quiz"))
    kb.row(InlineKeyboardButton(text="🏡 Главное меню", callback_data=f"user_back"))

    return kb.as_markup()