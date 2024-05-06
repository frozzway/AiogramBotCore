from aiogram.types import Message


class Stack:
    def __init__(self):
        self.items = []

    def is_empty(self):
        return not self.items

    def push(self, item: Message):
        self.items.append(item)

    def pop(self) -> Message:
        if not self.is_empty():
            return self.items.pop()
        raise IndexError("pop from empty stack")

    def size(self) -> int:
        return len(self.items)
