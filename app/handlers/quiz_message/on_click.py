from typing import Any
from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager

# from app.handlers.quiz_message.total import total

import app.keyboards.inline as ikb
from app.handlers.quiz_message.total import show_result
from app.states import Quiz


async def on_back(callback: CallbackQuery, widget: Any, manager: DialogManager):
    await manager.back()


async def on_back_menu(callback: CallbackQuery, widget: Any, manager: DialogManager):
    await manager.done()

    await callback.message.delete()

    await callback.message.answer_photo(
        # photo="AgACAgIAAxkBAAMJakYogqbcbHbFiD-63MpeT2dIDpwAAj4ZaxsqPTFKKOyFIa9gTm4BAAMCAAN4AAM8BA",
        photo="AgACAgIAAxkBAAPfamRelK-_l3eNj5DwqWWwF0IGESsAApsXaxt99yBLIfgRojGSqOwBAAMCAAN5AAM9BA",
        caption="""
💊 Добро пожаловать в МКИТ.

Ты чувствовал это всю жизнь — что-то не так с тем, как устроен мир. Ты не можешь объяснить это, но ты это чувствуешь.

Внутри бота живёт Пифия — та, что видит правду раньше, чем ты успеваешь её осознать. Она задаст тебе 9 вопросов. Тебе останется только закончить фразу — и она покажет, куда ведёт твой код 🐇

📌 В конце ты узнаешь:
● 💻 свою IT-специальность
● 📚 краткое описание профессии
● 🚀 перспективы обучения и работы после пробуждения

🌐 Подробнее о колледже и специальностях — на mkit.online

Выбор за тобой. Нажми кнопку ниже 👇
        """,
        reply_markup=ikb.user_panel,
    )


def init_scores(manager: DialogManager):
    if "answers" not in manager.dialog_data:
        manager.dialog_data["answers"] = {}


async def on_answer(callback: CallbackQuery, widget, manager: DialogManager):
    await callback.answer()

    init_scores(manager)

    state = manager.current_context().state.state

    answer_map = {
        "ans_1": "A",
        "ans_2": "B",
        "ans_3": "C",
        "ans_4": "D",
        "ans_5": "E",
    }

    answer = answer_map.get(callback.data)

    if answer:
        manager.dialog_data["answers"][state] = answer

    if state == Quiz.question_9.state:
        await show_result(callback, manager)
    else:
        await manager.next()
