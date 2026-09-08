from typing import Annotated
from datetime import datetime

from sqlalchemy import ForeignKey, String, BigInteger, DateTime
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

from config import config

engine = create_async_engine(url=config.database.sqlalchemy_url(),
                             echo=True)

async_session = async_sessionmaker(engine)

intpk = Annotated[int, mapped_column(primary_key=True)]


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[intpk]
    tg_id: Mapped[int] = mapped_column(BigInteger)
    first_name: Mapped[str] = mapped_column(String)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    quiz_completed_at: Mapped[datetime] = mapped_column(
        DateTime, default=None, nullable=True
    )


class Admin(Base):
    __tablename__ = 'admins'

    id: Mapped[intpk]
    tg_id: Mapped[int] = mapped_column(BigInteger)


async def create_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
