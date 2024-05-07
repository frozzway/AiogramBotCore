from aiogram.filters.callback_data import CallbackData


class Category(CallbackData, prefix='category'):
    id: int
