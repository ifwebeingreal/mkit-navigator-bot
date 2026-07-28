from aiogram import Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, StartMode, Dialog, Window
from aiogram_dialog.widgets.kbd import Button, Column
from aiogram_dialog.widgets.text import Const, Format

from app.states import Quiz

from app.handlers.quiz_message.on_click import (
    on_back_menu, on_back, on_answer
)
from app.handlers.quiz_message.getter import quiz_getter

from config import config
import app.keyboards.inline as ikb

quiz = Router()

quiz_dialog = Dialog(
    Window(
        Format(
            "{progress}\n\n"
            "🤖 Мне интересно разбираться, как устроены роботы, компьютеры, игры и другие технологии. "
            "Хочется понять, что находится «внутри» и как всё работает."
        ),
        Column(
            Button(Const("⭐ Очень похоже на меня"), id="ans_1", on_click=on_answer),
            Button(Const("🙂 Скорее похоже"), id="ans_2", on_click=on_answer),
            Button(Const("😐 Сложно сказать"), id="ans_3", on_click=on_answer),
            Button(Const("🙃 Скорее не про меня"), id="ans_4", on_click=on_answer),
            Button(Const("❌ Совсем не про меня"), id="ans_5", on_click=on_answer),
            Button(Const("⏪ Назад"), id="back_menu_btn", on_click=on_back_menu),
        ),
        state=Quiz.question_1,
        getter=quiz_getter
    ),
    Window(
        Format(
            "{progress}\n\n"
            "🧠 Мне интересно представить, что я создаю искусственный интеллект, "
            "который может помогать людям, решать задачи или учиться новому."
        ),
        Column(
            Button(Const("⭐ Очень похоже на меня"), id="ans_1", on_click=on_answer),
            Button(Const("🙂 Скорее похоже"), id="ans_2", on_click=on_answer),
            Button(Const("😐 Сложно сказать"), id="ans_3", on_click=on_answer),
            Button(Const("🙃 Скорее не про меня"), id="ans_4", on_click=on_answer),
            Button(Const("❌ Совсем не про меня"), id="ans_5", on_click=on_answer),
            Button(Const("⏪ Назад"), id="back", on_click=on_back),
            Button(Const("🏡 Главное меню"), id="back_menu_btn", on_click=on_back_menu),
        ),
        state=Quiz.question_2,
        getter=quiz_getter
    ),
    Window(
        Format(
            "{progress}\n\n"
            "🔐 3. Мне интересно защищать цифровой мир: находить слабые места"
            " в технологиях и делать так, чтобы данные людей были в безопасности."
        ),
        Column(
            Button(Const("⭐ Очень похоже на меня"), id="ans_1", on_click=on_answer),
            Button(Const("🙂 Скорее похоже"), id="ans_2", on_click=on_answer),
            Button(Const("😐 Сложно сказать"), id="ans_3", on_click=on_answer),
            Button(Const("🙃 Скорее не про меня"), id="ans_4", on_click=on_answer),
            Button(Const("❌ Совсем не про меня"), id="ans_5", on_click=on_answer),
            Button(Const("⏪ Назад"), id="back", on_click=on_back),
            Button(Const("🏡 Главное меню"), id="back_menu_btn", on_click=on_back_menu),
        ),
        state=Quiz.question_3,
        getter=quiz_getter
    ),
    Window(
        Format(
            "{progress}\n\n"
            "🧩 У меня развита логика. "
            "Если меня не отвлекать, я могу поэтапно решать сложные задачи."
        ),
        Column(
            Button(Const("⭐ Очень похоже на меня"), id="ans_1", on_click=on_answer),
            Button(Const("🙂 Скорее похоже"), id="ans_2", on_click=on_answer),
            Button(Const("😐 Сложно сказать"), id="ans_3", on_click=on_answer),
            Button(Const("🙃 Скорее не про меня"), id="ans_4", on_click=on_answer),
            Button(Const("❌ Совсем не про меня"), id="ans_5", on_click=on_answer),
            Button(Const("⏪ Назад"), id="back", on_click=on_back),
            Button(Const("🏡 Главное меню"), id="back_menu_btn", on_click=on_back_menu),
        ),
        state=Quiz.question_4,
        getter=quiz_getter
    ),
    Window(
        Format(
            "{progress}\n\n"
            "🎨 Мне нравится придумывать, как должны выглядеть приложения, сайты или игры: "
            "выбирать стиль, цвета, изображения и делать их удобными для людей."
        ),
        Column(
            Button(Const("⭐ Очень похоже на меня"), id="ans_1", on_click=on_answer),
            Button(Const("🙂 Скорее похоже"), id="ans_2", on_click=on_answer),
            Button(Const("😐 Сложно сказать"), id="ans_3", on_click=on_answer),
            Button(Const("🙃 Скорее не про меня"), id="ans_4", on_click=on_answer),
            Button(Const("❌ Совсем не про меня"), id="ans_5", on_click=on_answer),
            Button(Const("⏪ Назад"), id="back", on_click=on_back),
            Button(Const("🏡 Главное меню"), id="back_menu_btn", on_click=on_back_menu),
        ),
        state=Quiz.question_5,
        getter=quiz_getter
    ),
    Window(
        Format(
            "{progress}\n\n"
            "🛠 Мне нравится помогать другим, "
            "когда у них возникают проблемы с техникой, и находить способы всё исправить."
        ),
        Column(
            Button(Const("⭐ Очень похоже на меня"), id="ans_1", on_click=on_answer),
            Button(Const("🙂 Скорее похоже"), id="ans_2", on_click=on_answer),
            Button(Const("😐 Сложно сказать"), id="ans_3", on_click=on_answer),
            Button(Const("🙃 Скорее не про меня"), id="ans_4", on_click=on_answer),
            Button(Const("❌ Совсем не про меня"), id="ans_5", on_click=on_answer),
            Button(Const("⏪ Назад"), id="back", on_click=on_back),
            Button(Const("🏡 Главное меню"), id="back_menu_btn", on_click=on_back_menu),
        ),
        state=Quiz.question_6,
        getter=quiz_getter
    ),
    Window(
        Format(
            "{progress}\n\n"
            "🔎 Если передо мной появляется сложная задача, "
            "мне интересно искать разные варианты решения и не сдаваться, пока не получится."
        ),
        Column(
            Button(Const("⭐ Очень похоже на меня"), id="ans_1", on_click=on_answer),
            Button(Const("🙂 Скорее похоже"), id="ans_2", on_click=on_answer),
            Button(Const("😐 Сложно сказать"), id="ans_3", on_click=on_answer),
            Button(Const("🙃 Скорее не про меня"), id="ans_4", on_click=on_answer),
            Button(Const("❌ Совсем не про меня"), id="ans_5", on_click=on_answer),
            Button(Const("⏪ Назад"), id="back", on_click=on_back),
            Button(Const("🏡 Главное меню"), id="back_menu_btn", on_click=on_back_menu),
        ),
        state=Quiz.question_7,
        getter=quiz_getter
    ),
    Window(
        Format(
            "{progress}\n\n"
            "🚀 Мне хочется создавать что-то новое, "
            "чем смогут пользоваться другие люди: программы, игры, роботов, приложения или современные технологии."
        ),
        Column(
            Button(Const("⭐ Очень похоже на меня"), id="ans_1", on_click=on_answer),
            Button(Const("🙂 Скорее похоже"), id="ans_2", on_click=on_answer),
            Button(Const("😐 Сложно сказать"), id="ans_3", on_click=on_answer),
            Button(Const("🙃 Скорее не про меня"), id="ans_4", on_click=on_answer),
            Button(Const("❌ Совсем не про меня"), id="ans_5", on_click=on_answer),
            Button(Const("⏪ Назад"), id="back", on_click=on_back),
            Button(Const("🏡 Главное меню"), id="back_menu_btn", on_click=on_back_menu),
        ),
        state=Quiz.question_8,
        getter=quiz_getter
    ),
    Window(
        Format(
            "{progress}\n\n"
            "🖌️ Я творческий человек, мне близко искусство, в частности рисование."
        ),
        Column(
            Button(Const("⭐ Очень похоже на меня"), id="ans_1", on_click=on_answer),
            Button(Const("🙂 Скорее похоже"), id="ans_2", on_click=on_answer),
            Button(Const("😐 Сложно сказать"), id="ans_3", on_click=on_answer),
            Button(Const("🙃 Скорее не про меня"), id="ans_4", on_click=on_answer),
            Button(Const("❌ Совсем не про меня"), id="ans_5", on_click=on_answer),
            Button(Const("⏪ Назад"), id="back", on_click=on_back),
            Button(Const("🏡 Главное меню"), id="back_menu_btn", on_click=on_back_menu),
        ),
        state=Quiz.question_9,
        getter=quiz_getter
    ),
)


async def is_subscribed(bot, user_id: int, channel: str) -> bool:
    try:
        member = await bot.get_chat_member(chat_id=channel, user_id=user_id)
        return member.status in ("member", "administrator", "creator")
    except TelegramBadRequest:
        return False


@quiz.callback_query(F.data == "start_quiz")
async def quiz_callback(callback: CallbackQuery, dialog_manager: DialogManager):
    user_id = callback.from_user.id
    channel = config.bot.channel_id
    subscribed = await is_subscribed(callback.bot, user_id, channel)

    if not subscribed:
        # await callback.message.delete()  # решить убрать или оставить

        await callback.message.answer(
            """⚠️ Пифия пока тебя не видит.
Чтобы пройти тест, подпишись на наш канал — это твой ключ к системе.
После подписки нажми кнопку ещё раз 👇""",
            reply_markup=ikb.check_sub
        )
        print("CHECK SUBSCRIBE ON CHANNEL")
        await callback.answer()
        return

    await dialog_manager.start(Quiz.question_1, mode=StartMode.RESET_STACK)
    await callback.answer()


@quiz.callback_query(F.data == "check_sub")
async def quiz_callback(callback: CallbackQuery, dialog_manager: DialogManager):
    user_id = callback.from_user.id
    channel = config.bot.channel_id
    subscribed = await is_subscribed(callback.bot, user_id, channel)

    if not subscribed:
        await callback.answer(
            "🚫 Подключение не найдено. Система тебя не видит.",
            show_alert=True,
        )
        return

    await callback.message.edit_text("✅ Пифия тебя видит. Заходи.")
    await dialog_manager.start(Quiz.question_1, mode=StartMode.RESET_STACK)
    await callback.answer()
