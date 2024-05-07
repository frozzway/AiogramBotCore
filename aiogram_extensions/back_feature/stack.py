from dataclasses import dataclass

from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup


@dataclass
class MessageInfo:
    text: str | None = None
    reply_markup: InlineKeyboardMarkup | None = None


class Stack:
    def __init__(self):
        self.items = []

    def is_empty(self):
        return not self.items

    def push(self, item: MessageInfo):
        self.items.append(item)

    def pop(self) -> MessageInfo:
        if not self.is_empty():
            return self.items.pop()
        raise IndexError("pop from empty stack")

    def size(self) -> int:
        return len(self.items)

    def erase(self):
        self.items = []


async def erase_stack(state: FSMContext):
    state_data = await state.get_data()
    stack: Stack = state_data.get('message_stack')
    if stack:
        stack.erase()
        await state.update_data(message_stack=stack)
