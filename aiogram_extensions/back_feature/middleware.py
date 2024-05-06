from typing import Callable, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.dispatcher.flags import get_flag
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from .stack import Stack


class MessageSaverMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[CallbackQuery, dict[str, Any]], Awaitable[Any]],
            event: CallbackQuery,
            data: dict[str, Any]
    ) -> Any:
        state: FSMContext = data['state']
        state_data = await state.get_data()

        stack = state_data.get('message_stack')
        if not stack:
            stack = Stack()

        prev_message = event.message.model_copy(deep=True)

        message = await handler(event, data)

        flag = get_flag(data, 'DisableBackFromAhead')
        if message is not None and not flag:
            stack: Stack
            stack.push(prev_message)
            await state.update_data(message_stack=stack)
