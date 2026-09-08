import asyncio
from typing import Literal

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager

from app.database.requests.user.select import get_user
from app.database.requests.user.update import update_user_quiz_date

import app.keyboards.builder as bkb

RESULT_TEXT = {
    "prog": """
💻 <b>ТЫ ВИДИШЬ КОД. ТВОЙ ПУТЬ — РАЗРАБОТКА ПО</b>

Большинство людей смотрит на экран смартфона и видит просто иконки.

Ты же смотришь глубже — и видишь архитектуру, из которой всё это собрано.

За два с половиной года на специальности «Разработка и управление программным обеспечением» ты пройдёшь путь от первой строчки кода на Python до полноценных проектов.

Научишься проектировать базы данных, писать backend и frontend, собирать мобильные приложения и находить уязвимости в собственном же коде.

Здесь готовят не просто «кодеров», а архитекторов цифровых систем — тех, кто способен спроектировать CRM для бизнеса, интернет-магазин или бота с нуля и довести до реального запуска.

⚡ <b>Специальность МКИТ:</b>
09.02.11 Разработка и управление программным обеспечением

🔥 <b>Что тебя ждёт:</b>
• Python, Java, C#, SQL и работа с большими данными
• frontend и backend разработка сайтов и сервисов
• мобильная разработка кроссплатформенных приложений
• практика по Agile/Scrum, как в топовых IT-компаниях
• старт карьеры уже во время учёбы
""",
    "sec": """
🔐 <b>ТЫ — СТРАЖ СИСТЕМЫ. ТВОЙ ПУТЬ — КИБЕРБЕЗОПАСНОСТЬ</b>

Каждый день где-то в сети кто-то пытается вскрыть чужую систему.

Ты — один из немногих, кто видит эти трещины раньше, чем ими успевают воспользоваться.

На специальности «Обеспечение информационной безопасности автоматизированных систем» тебя научат искать уязвимости в сетях и базах данных, работать с криптографией, настраивать защиту серверов и техническую защиту информации.

Здесь важны хладнокровие, внимание к деталям и умение не паниковать, когда «всё упало» — ты станешь тем, кто чинит это спокойно и по шагам.

Практику можно проходить в банках, силовых структурах, медицинских и промышленных организациях — везде, где есть данные, которые нужно защищать.

⚡ <b>Специальность МКИТ:</b>
10.02.05 Информационная безопасность

🛡 <b>Что тебя ждёт:</b>
• поиск уязвимостей и анализ угроз
• криптографические и программно-аппаратные средства защиты
• администрирование сетей и баз данных
• карьера: инженер по защите информации, администратор ЛВС, разработчик баз данных
• дополнительная профессия «Оператор ЭВМ» уже в процессе учёбы
""",
    "sys": """
🛠 <b>ТЫ ДЕРЖИШЬ СИСТЕМУ В РАВНОВЕСИИ. ТВОЙ ПУТЬ — ТЕХНИЧЕСКАЯ ЭКСПЛУАТАЦИЯ</b>

Пока одни создают системы, а другие их взламывают — есть те, кто следит, чтобы вся конструкция не рухнула.

Это ты.

Специальность «Техническая эксплуатация и сопровождение информационных систем» готовит универсальных IT-специалистов: тех, кто устанавливает и настраивает серверы, администрирует базы данных, разворачивает сети и умеет объяснить обычному пользователю, что случилось с его компьютером, простыми словами.

Твоя миссия — сделать так, чтобы цифровая инфраструктура компании работала «как часы», а если что-то ломается — быстро вернуть систему к жизни.

⚡ <b>Специальность МКИТ:</b>
09.02.12 Системная эксплуатация и сопровождение ИС

🌐 <b>Что тебя ждёт:</b>
• установка и настройка серверов и сетей
• администрирование баз данных
• резервное копирование и защита от сбоев
• диагностика и устранение неполадок
• востребованность в любой сфере — от банков до промышленности
""",
    "des": """
🎨 <b>ТЫ ВИДИШЬ ФОРМУ ЗА КОДОМ. ТВОЙ ПУТЬ — ГРАФИЧЕСКИЙ ДИЗАЙН</b>

Система полна визуального шума.

Ты — один из тех редких людей, кто умеет превращать этот шум в порядок, стиль и смысл.

На специальности «Графический дизайнер» ты научишься работать в Photoshop, Illustrator, InDesign и After Effects, разбираться в типографике и теории цвета, создавать фирменный стиль, интерфейсы сайтов и мобильных приложений, упаковку и рекламные макеты.

Это творческая профессия, которая ценит и художественный вкус, и техническую точность — а дальше можно вырасти до арт- или креативного директора, уйти в геймдев, кино или рекламу.

⚡ <b>Специальность МКИТ:</b>
54.01.20 Графический дизайн

✨ <b>Что тебя ждёт:</b>
• Figma, Photoshop, Illustrator, After Effects
• фирменный стиль, брендинг, упаковка
• UI/UX для сайтов и приложений
• карьера: от дизайнера до арт-директора
""",
    "none": """
🤔 <b>СИСТЕМА В ЗАДУМЧИВОСТИ...</b>

Мы не можем поверить, что тебя не привлекает IT...

По твоим ответам пока сложно определить направление. Но это не значит, что Матрица не для тебя!

Попробуй изучить разные направления и найти то, что действительно откликается 🚀
""",
}

Answer = Literal["A", "B", "C", "D", "E"]
Specialty = Literal["prog", "sec", "des", "sys", "none"]

# Чем БОЛЬШЕ число — тем сильнее ответ.
ANSWER_RANK: dict[Answer, int] = {
    "A": 5,
    "B": 4,
    "C": 3,
    "D": 2,
    "E": 1,
}

# Вопросы, которые характеризуют каждое направление.
# Используем их только для определения приоритета,
# если пользователю подходят сразу несколько направлений.
SPECIALTY_QUESTIONS: dict[str, tuple[int, ...]] = {
    "prog": (1, 2, 4, 7, 8),
    "sec": (1, 3, 4, 7),
    "des": (5, 9),
    "sys": (1, 6),
}


def normalize_answers(answers: dict) -> dict[str, Answer]:
    """
    Приводит:

        Quiz:question_1 -> question_1

    к единому формату.
    """

    normalized = {}

    for key, value in answers.items():
        question = str(key).split(":")[-1]

        if value in ANSWER_RANK:
            normalized[question] = value

    return normalized


def validate_answers(answers: dict[str, Answer]) -> None:
    """
    Проверяем, что пользователь действительно
    ответил на все 9 вопросов.
    """

    required_questions = {f"question_{number}" for number in range(1, 10)}

    missing = required_questions - answers.keys()

    if missing:
        raise ValueError(f"Не получены ответы на вопросы: {sorted(missing)}")


def answer(
    answers: dict[str, Answer],
    question: int,
) -> Answer:
    return answers[f"question_{question}"]


def is_stronger(
    first: Answer,
    second: Answer,
) -> bool:
    """
    A сильнее B, B сильнее C и т.д.
    """

    return ANSWER_RANK[first] > ANSWER_RANK[second]


# ============================================================
# РАЗРАБОТКА ПО
# ============================================================


def matches_programming(
    answers: dict[str, Answer],
) -> tuple[bool, bool]:
    """
    Возвращает:

        (подходит_разработка, нужен_fallback)

    fallback нужен в ситуации, когда базовые критерии
    разработчика выполнены, но среди 1, 2 и 8 вопросов
    два или более ответа C.
    """

    q1 = answer(answers, 1)
    q2 = answer(answers, 2)
    q4 = answer(answers, 4)
    q7 = answer(answers, 7)
    q8 = answer(answers, 8)

    # Если вопрос 8 = A,
    # направление разработки обязательно рассматриваем.
    if q8 == "A":
        return True, False

    base_match = (
        q1 in {"A", "B", "C"}
        and q2 in {"A", "B", "C"}
        and q4 in {"A", "B", "C"}
        and q7 in {"A", "B", "C", "D"}
        and q8 in {"A", "B", "C"}
    )

    if not base_match:
        return False, False

    c_count = sum(value == "C" for value in (q1, q2, q8))

    if c_count >= 2:
        return False, True

    return True, False


# ============================================================
# ИНФОРМАЦИОННАЯ БЕЗОПАСНОСТЬ
# ============================================================


def matches_security(
    answers: dict[str, Answer],
) -> bool:
    q1 = answer(answers, 1)
    q3 = answer(answers, 3)
    q4 = answer(answers, 4)
    q7 = answer(answers, 7)

    return (
        q1 in {"A", "B"}
        and q3 in {"A", "B"}
        and q4 in {"A", "B", "C"}
        and q7 in {"A", "B", "C"}
    )


def has_security_priority(
    answers: dict[str, Answer],
) -> bool:
    """
    Дополнительный критерий:

    если ответ на вопрос 3 сильнее,
    чем на 1, 2 или 8, это усиливает
    направление информационной безопасности.

    ВАЖНО:
    это приоритет, а не обязательное условие
    для попадания в информационную безопасность.
    """

    q3 = answer(answers, 3)

    return any(is_stronger(q3, answer(answers, question)) for question in (1, 2, 8))


# ============================================================
# ГРАФИЧЕСКИЙ ДИЗАЙН
# ============================================================


def matches_design(
    answers: dict[str, Answer],
) -> bool:
    q1 = answer(answers, 1)
    q3 = answer(answers, 3)
    q5 = answer(answers, 5)
    q8 = answer(answers, 8)
    q9 = answer(answers, 9)

    return (
        q5 in {"A", "B", "C"}
        and q9 in {"A", "B", "C"}
        and q1 in {"C", "D", "E"}
        and q3 in {"C", "D", "E"}
        and q8 in {"C", "D", "E"}
        and (q5 in {"A", "B"} or q9 in {"A", "B"})
    )


# ============================================================
# ТЕХНИЧЕСКАЯ ЭКСПЛУАТАЦИЯ
# ============================================================


def matches_systems(
    answers: dict[str, Answer],
) -> bool:
    q1 = answer(answers, 1)
    q6 = answer(answers, 6)

    if q1 not in {"A", "B", "C"} or q6 not in {"A", "B", "C"}:
        return False

    c_count = sum(value == "C" for value in (q1, q6))

    return c_count <= 1


# ============================================================
# "IT НЕ ПРИВЛЕКАЕТ"
# ============================================================


def matches_none(
    answers: dict[str, Answer],
) -> bool:
    """
    Согласно текущим критериям:

    1, 2, 3, 5, 6 = C/D/E.

    Вопросы 4 и 7 не учитываются.
    """

    return all(
        answer(answers, question) in {"C", "D", "E"} for question in (1, 2, 3, 5, 6)
    )


# ============================================================
# FALLBACK РАЗРАБОТЧИКА
# ============================================================


def get_programming_fallback(
    answers: dict[str, Answer],
) -> Specialty | None:
    """
    Используется, когда:

    Q1/Q2/Q8 подходят разработчику,
    но среди них >= 2 ответов C.

    Тогда смотрим самые сильные ответы:

    Q3 -> информационная безопасность
    Q5/Q9 -> дизайн
    Q6 -> эксплуатация

    Рассматриваем только A/B.
    """

    candidates: dict[Specialty, int] = {
        "sec": ANSWER_RANK[answer(answers, 3)],
        "des": max(
            ANSWER_RANK[answer(answers, 5)],
            ANSWER_RANK[answer(answers, 9)],
        ),
        "sys": ANSWER_RANK[answer(answers, 6)],
    }

    # По ТЗ альтернативный ответ
    # должен быть минимум B.
    candidates = {
        specialty: score
        for specialty, score in candidates.items()
        if score >= ANSWER_RANK["B"]
    }

    if not candidates:
        return None

    max_score = max(candidates.values())

    best = [specialty for specialty, score in candidates.items() if score == max_score]

    if len(best) == 1:
        return best[0]

    # Если одинаковый ответ, используем общий
    # профиль специальности как tie-break.
    best.sort(
        key=lambda specialty: specialty_strength(
            specialty,
            answers,
        ),
        reverse=True,
    )

    return best[0]


# ============================================================
# СРАВНЕНИЕ ДВУХ СПЕЦИАЛЬНОСТЕЙ
# ============================================================


def specialty_strength(
    specialty: Specialty,
    answers: dict[str, Answer],
) -> tuple[int, int, int, int]:
    """
    Правило приоритета:

    1. больше A
    2. больше B
    3. больше C
    4. общий балл

    Первые два пункта соответствуют ТЗ заказчика.
    C и общий балл используются только как технический
    tie-break, чтобы результат всегда был детерминирован.
    """

    questions = SPECIALTY_QUESTIONS.get(specialty, ())

    values = [answer(answers, question) for question in questions]

    a_count = values.count("A")
    b_count = values.count("B")
    c_count = values.count("C")

    total_score = sum(ANSWER_RANK[value] for value in values)

    return (
        a_count,
        b_count,
        c_count,
        total_score,
    )


def sort_results(
    results: set[Specialty],
    answers: dict[str, Answer],
) -> list[Specialty]:
    """
    Сортируем результаты согласно правилу:
    больше A -> больше B.

    Если всё равно равенство —
    используется C и суммарная сила ответов.
    """

    return sorted(
        results,
        key=lambda specialty: specialty_strength(
            specialty,
            answers,
        ),
        reverse=True,
    )


# ============================================================
# ОСНОВНАЯ ЛОГИКА
# ============================================================


def get_result(raw_answers: dict) -> list[Specialty]:
    answers = normalize_answers(raw_answers)

    validate_answers(answers)

    results: set[Specialty] = set()

    # --------------------------------------------------------
    # 1. Разработка
    # --------------------------------------------------------

    programming, programming_fallback = matches_programming(answers)

    if programming:
        results.add("prog")

    # --------------------------------------------------------
    # 2. Информационная безопасность
    # --------------------------------------------------------

    security = matches_security(answers)

    if security:
        results.add("sec")

    # --------------------------------------------------------
    # 3. Графический дизайн
    # --------------------------------------------------------

    design = matches_design(answers)

    if design:
        results.add("des")

    # --------------------------------------------------------
    # Специальный fallback разработчика
    # --------------------------------------------------------

    if programming_fallback:
        fallback = get_programming_fallback(answers)

        if fallback is not None:
            results.add(fallback)

    # --------------------------------------------------------
    # 4. Техническая эксплуатация
    #
    # По ТЗ добавляем её только тогда,
    # когда пользователь НЕ прошёл критерии
    # первых трёх направлений.
    # --------------------------------------------------------

    if not results and matches_systems(answers):
        results.add("sys")

    # --------------------------------------------------------
    # 6. IT не привлекает
    #
    # ВАЖНО:
    # проверяется ПОСЛЕ специальностей.
    #
    # Иначе старая реализация могла вернуть none
    # даже при наличии валидного результата.
    # --------------------------------------------------------

    if not results and matches_none(answers):
        return ["none"]

    # Если вообще ничего не подошло.
    if not results:
        return ["none"]

    # --------------------------------------------------------
    # Сортировка при совпадениях
    # --------------------------------------------------------

    sorted_results = sort_results(
        results,
        answers,
    )

    # По текущей логике квиза пользователю имеет смысл
    # показывать максимум два наиболее подходящих направления.
    return sorted_results[:2]


# ============================================================
# ВЫВОД РЕЗУЛЬТАТА
# ============================================================


async def show_result(
    callback: CallbackQuery,
    manager: DialogManager,
):
    raw_answers = manager.dialog_data.get(
        "answers",
        {},
    )

    user = await get_user(
        callback.from_user.id,
    )

    if not user.quiz_completed_at:
        await update_user_quiz_date(
            callback.from_user.id,
        )

    msg = await callback.message.edit_text(
        "🔮 Пифия закрывает глаза — " "она услышала достаточно..."
    )

    await asyncio.sleep(1.2)

    await msg.edit_text("💻 ...и уже видит, куда на самом деле " "ведёт твой путь.")

    await asyncio.sleep(1.2)

    try:
        results = get_result(
            raw_answers,
        )
    except ValueError as error:
        print(f"Ошибка подсчёта квиза " f"user_id={callback.from_user.id}: " f"{error}")

        await manager.done()

        await msg.edit_text(
            "⚠️ Не удалось определить результат теста.\n\n"
            "Попробуй пройти его ещё раз."
        )

        await callback.answer()
        return

    await manager.done()

    print(f"user_id={callback.from_user.id}")
    print(f"answers={normalize_answers(raw_answers)}")
    print(f"results={results}")

    # Один результат
    if len(results) == 1:
        key = results[0]

        await msg.edit_text(
            RESULT_TEXT[key],
            reply_markup=await bkb.result_panel(
                key,
            ),
        )

        await callback.answer()
        return

    # Несколько результатов
    text = "🎯 <b>Тебе подходят несколько направлений:</b>\n\n"

    for key in results:
        text += RESULT_TEXT[key].strip() + "\n\n"

    await msg.edit_text(
        text.strip(),
        reply_markup=await bkb.result_panel(
            results[0],
        ),
    )

    await callback.answer()
