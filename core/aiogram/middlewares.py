from typing import Callable, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.exceptions import TelegramAPIError

from core.database import AsyncSessionMaker
from core.managers import CategoryManager


class DependencyInjectionMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message | CallbackQuery, dict[str, Any]], Awaitable[Any]],
            event: Message | CallbackQuery,
            data: dict[str, Any]
    ) -> Any:
        async with AsyncSessionMaker() as session:
            data['category_manager'] = CategoryManager(session)
            await handler(event, data)


class MessageEraserMiddleware(BaseMiddleware):
    """Удаляет ранее отправленное ботом сообщение при запросе нового. Чаще всего применяется для команды /menu, чтобы
    не плодить сообщения в чате с главным меню."""
    async def __call__(
            self,
            handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: dict[str, Any]
    ) -> Any:
        state: FSMContext = data['state']
        state_data = await state.get_data()
        if last_message := state_data.get('last_message'):
            try:
                await last_message.delete()
            except TelegramAPIError:
                pass
        message = await handler(event, data)
        await state.update_data(last_message=message)
