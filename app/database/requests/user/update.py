from datetime import datetime

from app.database.models import async_session
from app.database.models import User
from sqlalchemy import update


async def update_user_quiz_date(tg_id: int):
    async with async_session() as session:
        await session.execute(
            update(User)
            .where(User.tg_id == tg_id)
            .values(quiz_completed_at=datetime.now())
        )
        await session.commit()
