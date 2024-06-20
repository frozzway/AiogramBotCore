from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from core.settings import settings


class Base(DeclarativeBase):
    pass


url_params = {
    'username': settings.db_username,
    'password': settings.db_password,
    'host': settings.db_host,
    'port': settings.db_port,
    'database': settings.db_database
}

async_url_object = URL.create(
    'postgresql+asyncpg',
    **url_params
)

main_thread_async_engine = create_async_engine(async_url_object, pool_size=5, max_overflow=0, pool_timeout=3600)

AsyncSessionMaker = async_sessionmaker(main_thread_async_engine, expire_on_commit=False)
