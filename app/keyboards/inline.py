from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from config import config

admin_panel = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Рассылка", callback_data="sender")],
        [InlineKeyboardButton(text="Администраторы", callback_data="admins")],
    ]
)

admin_cancel = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🔙 Назад", callback_data="back")]
    ]
)

user_panel = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="💊 Принять красную таблетку", callback_data="start_quiz")],
    ]
)

user_cancel = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="❌ Отменить", callback_data="user_cancel")]
    ]
)

data_panel = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="✅ Отправить", callback_data="finally_send")],
        [InlineKeyboardButton(text="📃Политика обработки", url="https://mkit.online/#policy")],
        [InlineKeyboardButton(text="❌ Отменить", callback_data="user_cancel")],
    ]
)

user_back_to_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🏡 Вернуться в меню", callback_data="user_back_to_menu")]
    ]
)

check_sub = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Подписаться", url=config.bot.channel_link)],
        [InlineKeyboardButton(text="Проверить подключение", callback_data="check_sub")]
    ]
)
