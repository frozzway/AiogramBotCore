from aiogram.filters.callback_data import CallbackData


class Category(CallbackData, prefix='category'):
    """Коллбэк для перехода в категорию по её идентификатору"""
    id: int
