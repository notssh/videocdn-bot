from sqlalchemy import Integer, Column, DateTime, MetaData, update, inspect, select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import datetime as dt
import consts

async_engine = create_async_engine(consts.database_url)
Base = declarative_base()
metadata = MetaData()
AsyncSession = sessionmaker(bind=async_engine, expire_on_commit=False, class_=AsyncSession)
session = AsyncSession()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer(), primary_key=True, unique=True)
    start_usage_count = Column(Integer(), nullable=False, default=0)
    short_usage_count = Column(Integer(), nullable=False, default=0)
    inline_usage_count = Column(Integer(), nullable=False, default=0)
    created_on = Column(DateTime(), default=dt.datetime.now())
    updated_on = Column(DateTime(), default=dt.datetime.now(), onupdate=dt.datetime.now())


def tables_is_installed(connection):
    if inspect(connection).has_table(session, 'users'):
        return True
    return False


async def setup_db_if_required():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        return True


async def recreate_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def update_user_usage_count(user_id: int, used: str):
    user = (await session.execute(select(User).filter(User.id == user_id))).all()
    if not user:
        session.add(User(id=user_id))
        await session.commit()
    if used == 'start':
        await session.execute(update(User).where(User.id == user_id).values(start_usage_count=User.start_usage_count+1))
    elif used == 'short':
        await session.execute(update(User).where(User.id == user_id).values(short_usage_count=User.short_usage_count+1))
    elif used == 'inline':
        await session.execute(update(User).where(User.id == user_id).values(inline_usage_count=User.inline_usage_count+1))
    await session.commit()
