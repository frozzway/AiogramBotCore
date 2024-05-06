from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder


class BackCallback(CallbackData, prefix='back_feature-back-button'):
    pass


back_button = InlineKeyboardBuilder()
back_button.button(text='Назад', callback_data=BackCallback())
