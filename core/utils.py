import asyncio
import functools
import logging
from datetime import datetime
from typing import TypeVar

import httpx
from dateutil.relativedelta import relativedelta
from loguru import logger


T = TypeVar('T')

api_semaphore = asyncio.Semaphore(10)
telegram_semaphore = asyncio.Semaphore(10)
db_semaphore = asyncio.Semaphore(10)


def yesterday() -> datetime:
    now = datetime.today()
    return now.replace(hour=0, minute=0, second=0, microsecond=0) - relativedelta(days=1)


def api_call(handle_errors: bool = False, log_level=logging.ERROR, target_api_prefix='Энергоатлас API',
             telegram_call=False):
    """Декоратор для асинхронных атомарных методов, выполняющих запросы к API внешней системы / Telegram. Ограничивает количество
    одновременных запросов в соответствии со значением семафора и логирующий Http-исключения и ответы с кодом 4хх-5хх.
    :param handle_errors: писать информацию в лог, при выброшенном исключении, подменяя возвращаемое значение метода на None
    :param log_level: уровень логов
    :param telegram_call: обращение к API Telegram
    :param target_api_prefix: Строка-префикс - название ресурса для указания в логах
    """
    sem = telegram_semaphore if telegram_call else api_semaphore
    target_api_prefix = 'Telegram API' if telegram_call else target_api_prefix

    def wrapper(func):
        @functools.wraps(func)
        async def wrapped(*args, **kwargs):
            async with sem:
                if handle_errors:
                    try:
                        return await func(*args, **kwargs)
                    except httpx.HTTPStatusError as exc:
                        logger.log(log_level, f'[{target_api_prefix}] HTTP error {exc.response.status_code} - {exc.response.reason_phrase} on url {exc.request.url}')
                        raise exc
                    except httpx.RequestError as exc:
                        logger.log(log_level, f'[{target_api_prefix}] {exc} {type(exc)}'.strip())
                        raise exc
                else:
                    return await func(*args, **kwargs)
        return wrapped
    return wrapper
