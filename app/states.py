from aiogram.fsm.state import State, StatesGroup


class AddAdmin(StatesGroup):
    tg_id = State()


class SendAll(StatesGroup):
    text = State()


class Quiz(StatesGroup):
    question_1 = State()
    question_2 = State()
    question_3 = State()
    question_4 = State()
    question_5 = State()
    question_6 = State()
    question_7 = State()
    question_8 = State()
    question_9 = State()


class SendRequest(StatesGroup):
    name = State()
    phone = State()
    confirm = State()
