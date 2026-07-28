from aiogram_dialog import DialogManager


def get_progress_text(manager: DialogManager) -> str:
    states = {
        "question_1": 1,
        "question_2": 2,
        "question_3": 3,
        "question_4": 4,
        "question_5": 5,
        "question_6": 6,
        "question_7": 7,
        "question_8": 8,
        "question_9": 9,
    }

    current_state = str(manager.current_context().state)

    for state_name, number in states.items():
        if state_name in current_state:
            current = number
            break
    else:
        current = 1

    total = 9

    filled = "🟦" * current
    empty = "⬜" * (total - current)

    return (
        f"🔮 <b>Пифия слушает. Вопрос {current}/{total}</b>\n"
        f"{filled}{empty}"
    )


async def quiz_getter(dialog_manager: DialogManager, **kwargs):
    return {
        "progress": get_progress_text(dialog_manager)
    }