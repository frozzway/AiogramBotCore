from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup

from aiogram_extensions import back_feature
from aiogram_extensions.paginator import PaginatedKeyboard

from core.aiogram.callbacks import Category
from core.aiogram.middlewares import MessageEraserMiddleware
from core.managers import CategoryManager
from core.tables import Category as CategoryTable, ScenarioButton, LinkButton, Element


category_router = Router(name='category_router')
category_router.message.middleware(MessageEraserMiddleware())

main_category = InlineKeyboardBuilder()
main_category.button(text='Главное меню', callback_data=Category(id=1))
post_buttons = back_feature.back_button.copy()
post_buttons.attach(main_category)
post_buttons.adjust(1, 1)


@category_router.callback_query(Category.filter())
async def render_category(event: CallbackQuery, state: FSMContext, callback_data: Category,
                          category_manager: CategoryManager):
    """Отобразить категорию по нажатию на кнопку с её наименованием"""
    category = await category_manager.get_category(callback_data.id)
    elements = await category_manager.get_child_elements(category.id)
    markup = _get_category_markup(elements)
    keyboard = InlineKeyboardBuilder(markup=markup.inline_keyboard)

    if category.id == 1:
        await back_feature.erase_stack(state)

    post = post_buttons if category.id != 1 else None
    keyboard = await PaginatedKeyboard.create(keyboard=keyboard, state=state, page_size=category.page_size,
                                              post=post, unique_name='Меню категории')

    message = await event.message.edit_text(text=get_category_text(category), reply_markup=keyboard.first_page(),
                                            parse_mode='HTML')
    return message


@category_router.message(Command('menu'))
async def render_main_category(event: Message, state: FSMContext, category_manager: CategoryManager):
    """Отобразить главную категорию по команде /menu"""
    await back_feature.erase_stack(state)
    category = await category_manager.get_category(1)
    elements = await category_manager.get_child_elements(category.id)
    markup = _get_category_markup(elements)
    keyboard = InlineKeyboardBuilder(markup=markup.inline_keyboard)

    keyboard = await PaginatedKeyboard.create(keyboard=keyboard, state=state, page_size=category.page_size,
                                              unique_name='Меню категории')
    message = await event.answer(text=get_category_text(category), reply_markup=keyboard.first_page(),
                                 parse_mode='HTML')
    return message


def _get_button_from_element(item: Element) -> InlineKeyboardButton:
    if isinstance(item, CategoryTable):
        return InlineKeyboardButton(text=item.name, callback_data=Category(id=item.id).pack())
    if isinstance(item, LinkButton):
        return InlineKeyboardButton(text=item.name, url=item.url)
    if isinstance(item, ScenarioButton):
        return InlineKeyboardButton(text=item.name, callback_data=item.callback_url)
    else:
        raise TypeError(f'Item type {type(item)} not supported')


def _get_category_markup(elements: list[list[Element]]) -> InlineKeyboardMarkup:
    result = []
    for row in elements:
        res_row = []
        for item in row:
            button = _get_button_from_element(item)
            res_row.append(button)
        result.append(res_row)
    return InlineKeyboardMarkup(inline_keyboard=result)


def get_category_text(category: CategoryTable) -> str:
    text = f'<b><u>{category.name}</u></b>'
    if category.text:
        text += f'\n{category.text}'
    return text
