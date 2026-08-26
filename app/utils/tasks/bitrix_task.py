import asyncio

from bitrix24 import Bitrix24

from app.utils.tasks.celery_core import celery_app
from config import config


async def _save_lead_to_bitrix(
        name: str,
        phone: str,
        speciality: str,
):
    bx24 = Bitrix24(config.bitrix.bitrix_webhook_url)

    new_lead_data = {
        "fields": {
            "TITLE": "Заявка из бота",
            "NAME": name,
            "STATUS_ID": "NEW",
            "OPENED": "Y",
            "PHONE": [
                {
                    "VALUE": phone,
                    "VALUE_TYPE": "WORK",
                }
            ],
            "COMMENTS": f"Направление: {speciality}",
        }
    }

    try:
        result = await bx24.callMethod(
            "crm.lead.add",
            **new_lead_data,
        )

        print(
            f"Лид успешно добавлен! "
            f"ID нового лида: {result}"
        )

    except Exception as e:
        print(f"Ошибка при добавлении лида: {e}")
        raise


@celery_app.task(name="save_lead_to_bitrix")
def save_lead_to_bitrix(
        name: str,
        phone: str,
        speciality: str,
):
    asyncio.run(
        _save_lead_to_bitrix(
            name=name,
            phone=phone,
            speciality=speciality,
        )
    )
