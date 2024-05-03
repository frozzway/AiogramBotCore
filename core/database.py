from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import async_sessionmaker

from core.settings import settings


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

main_thread_async_engine = create_async_engine(async_url_object)

AsyncSessionMaker = async_sessionmaker(main_thread_async_engine, expire_on_commit=False)
