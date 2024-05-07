from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from .callback import BackCallback
from .stack import Stack


router = Router(name=__name__)


@router.callback_query(BackCallback.filter())
async def render_previous_message(query: CallbackQuery, state: FSMContext):
    """Метод отрисовывающий последнее сообщение, хранящееся в стеке"""
    data = await state.get_data()

    stack = data.get('message_stack')
    if not isinstance(stack, Stack):
        return
    if stack.is_empty():
        await query.answer('Назад вернуться невозможно. Начните сначала')
        return None

    message = stack.pop()
    await state.update_data(message_stack=stack)

    await query.message.edit_text(text=message.text, reply_markup=message.reply_markup, parse_mode='HTML')
