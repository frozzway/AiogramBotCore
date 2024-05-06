import asyncio

from aiogram import Dispatcher, Bot, Router
from aioshedule import Scheduler
from loguru import logger

from aiogram_extensions.paginator import router as paginator_router
from aiogram_extensions.back_feature import router as back_feature_router
from aiogram_extensions.back_feature import MessageSaverMiddleware

from core.aiogram import router as app_router
from core.aiogram.middlewares import DependencyInjectionMiddleware
from core.dependencies import http_client
from core.database import main_thread_async_engine
from core.tables import Base
from core.settings import settings


router = Router(name=__name__)
router.include_router(paginator_router)
router.include_router(back_feature_router)
router.include_router(app_router)

router.callback_query.middleware(DependencyInjectionMiddleware())
router.callback_query.middleware(MessageSaverMiddleware())
router.message.middleware(DependencyInjectionMiddleware())

bot = Bot(token=settings.bot_token)


async def on_startup(dispatcher: Dispatcher):
    await create_tables()
    http_client_dependency = http_client()
    client = await anext(http_client_dependency)
    _ = asyncio.create_task(run_scheduled_tasks())
    logger.info('Started polling...')
    await bot.set_my_commands(settings.bot_commands)
    await dispatcher.start_polling(bot, http_client=client)


async def run_scheduled_tasks():
    schedule = Scheduler()

    schedule.every().day.do(asyncio.sleep, 1)
    schedule.every().minute.do(asyncio.sleep, 30)

    logger.info('Started background tasks...')

    while True:
        await schedule.run_pending()
        await asyncio.sleep(1)


async def create_tables():
    async with main_thread_async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def main():
    dispatcher = Dispatcher()
    dispatcher.include_router(router)
    await on_startup(dispatcher)


if __name__ == '__main__':
    asyncio.run(main())