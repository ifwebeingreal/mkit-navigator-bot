from aiogram import Router, Bot, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

import app.keyboards.reply as rkb
import app.keyboards.inline as ikb
import app.keyboards.builder as bkb

from app.states import SendRequest

from app.utils.tasks.bitrix_task import save_lead_to_bitrix

from config import config

request = Router()


@request.callback_query(F.data.startswith("send_request_"))
async def start_send_request(callback: CallbackQuery, state: FSMContext):
    key = callback.data.split("_")[2]

    if key == "dec":
        await state.update_data(key="🎨 Графический дизайн (54.01.20)")
    elif key == "sys":
        await state.update_data(key="🛠 Системная эксплуатация (09.02.12)")
    elif key == "sec":
        await state.update_data(key="🔐 Информационная безопасность (10.02.05)")
    elif key == "prog":
        await state.update_data(key="💻 Программирование (09.02.11)")
    elif key == "none":
        await state.update_data(key="Не определено")

    await callback.message.answer(
        """🔮 Пифия улыбается: «Я вижу твой путь. Осталось узнать твоё имя».
✨ Как к тебе обращаться? Напиши своё имя 👇""",
        reply_markup=ikb.user_cancel,
    )

    await state.set_state(SendRequest.name)


@request.message(SendRequest.name)
async def check_name(message: Message, state: FSMContext):
    if message.text and len(message.text) <= 200:
        await state.update_data(name=message.text)

        await message.answer(
            """🔮 «Почти всё решено. Дай мне способ с тобой связаться».
📞 Оставь свой номер телефона, чтобы мы могли с тобой связаться 👇""",
            reply_markup=ikb.user_cancel,
        )

        await state.set_state(SendRequest.phone)

    else:
        await message.answer(
            "<b>Имя должно быть до 200 символов!</b>", reply_markup=ikb.user_cancel
        )


@request.message(SendRequest.phone)
async def check_phone(message: Message, state: FSMContext):
    if message.text and len(message.text) <= 15:
        await state.update_data(phone=message.text)

        await message.answer(
            "<b>📌 Подтверждение заявки</b>\n\n"
            "Нажимая «Отправить», ты даёшь согласие на обработку персональных данных\n"
            "и подтверждаешь отправку заявки в приёмную комиссию МКИТ.",
            reply_markup=ikb.data_panel,
        )

        await state.set_state(SendRequest.confirm)

    else:
        await message.answer(
            "<b>Номер телефона должен быть короче 15 символов!</b>",
            reply_markup=ikb.user_cancel,
        )


@request.callback_query(F.data == "finally_send", SendRequest.confirm)
async def finally_send(callback: CallbackQuery, state: FSMContext, bot: Bot):
    await callback.message.answer(
        "<b>🎉 Заявка успешно отправлена!</b>\n\n"
        "Спасибо за интерес к МКИТ 🙌\n"
        "Мы уже передали твою заявку в приёмную комиссию.\n\n"
        "📞 В ближайшее время с тобой свяжется специалист и расскажет все детали поступления.\n\n"
        "🌐 А пока можешь заглянуть на mkit.online — там подробно про каждую специальность, стоимость обучения и день открытых дверей.",
        reply_markup=ikb.user_back_to_menu,
        disable_web_page_preview=True,
    )

    data = await state.get_data()

    key = data.get("key")
    name = data.get("name")
    phone = data.get("phone")

    admin_text = (
        "📥 <b>Новая заявка с квиза МКИТ</b>\n\n"
        f"🎯 <b>Направление:</b> {key}\n\n"
        f"👤 <b>Имя:</b> {name}\n"
        f"📞 <b>Телефон:</b> {phone}\n\n"
        "👤 <b>Данные Telegram</b>\n"
        f"• ID: <code>{callback.from_user.id}</code>\n"
        f"• Имя в Telegram: {callback.from_user.full_name}\n"
        f"• Username: @{callback.from_user.username if callback.from_user.username else 'отсутствует'}\n"
        "\n——————————————\n"
        "⚡ <b>Источник:</b> Telegram Quiz Bot"
    )

    await bot.send_message(chat_id=config.bot.request_chat_id, text=admin_text)

    save_lead_to_bitrix.delay(name=name, phone=phone, speciality=key)

    await state.clear()
