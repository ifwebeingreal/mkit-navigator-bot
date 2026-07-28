from aiogram import Router, Bot, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

import app.keyboards.reply as rkb
import app.keyboards.inline as ikb
import app.keyboards.builder as bkb

from app.database.requests.admin.select import get_admins
from app.database.requests.user.add import set_user

user = Router()


# @user.message(F.photo)
# async def get_photo_id(message: Message):
#     await message.answer(message.photo[-1].file_id)


# @user.callback_query(F.data == "check_sub")
# async def check_sub(callback: CallbackQuery):
#     await callback.message.edit_text("Спасибо за подписку, вы можете пользоваться ботом!")
#
#     await set_user(callback.from_user.id, callback.from_user.full_name)


@user.message(CommandStart())
async def start_command(message: Message):
    await set_user(message.from_user.id, message.from_user.full_name)

    await message.answer_photo(
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
    reply_markup=ikb.user_panel)

    admins = await get_admins()

    for admin in admins:
        if admin.tg_id == message.from_user.id:
            await message.answer(f"Вы успешно авторизовались как администратор!",
                                 reply_markup=rkb.admin_menu)
            return


@user.callback_query(F.data == "user_back")
async def user_back(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
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
        reply_markup=ikb.user_panel)

    await state.clear()


@user.callback_query(F.data == "user_back_to_menu")
async def user_back_to_menu(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

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
        reply_markup=ikb.user_panel)

    await state.clear()


@user.callback_query(F.data == "user_cancel")
async def user_cancel(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.delete()