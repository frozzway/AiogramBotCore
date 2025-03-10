from __future__ import annotations

from aiogram.fsm.context import FSMContext
from aiogram_extensions.paginator.callback import Page
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup, InlineKeyboardButton


class PaginatedKeyboard:
    @classmethod
    async def create(cls, keyboard: InlineKeyboardBuilder, unique_name: str, state: FSMContext, page_size: int | None = 10,
                     pre: InlineKeyboardBuilder | None = None, post: InlineKeyboardBuilder | None = None,
                     text: str | None = None, parse_mode: str = 'HTML') -> PaginatedKeyboard:
        """
        Клавиатура с пагинацией.
        :param keyboard: объект, подвергающийся пагинации.
        :param unique_name: уникальное наименование клавиатуры.
        :param page_size: количество кнопок на одной странице, без учета статического блока.
        :param pre: статический блок кнопок, который будет добавлен перед списком элементов на каждой странице.
        :param post: статический блок кнопок, который будет добавлен после навигационной строки на каждой странице.
        :param text: текст, который отправлялся вместе с клавиатурой в обработчике, где клавиатура была инициализирована.
        :param parse_mode: форматирование текста.
        """
        if page_size is None:
            page_size = 1000
        self = cls(keyboard=keyboard, name=unique_name, state=state, page_size=page_size, pre=pre, post=post, text=text,
                   parse_mode=parse_mode)
        await self._write_keyboard_to_state()
        await state.update_data(last_paginated_keyboard=self)
        return self

    def __init__(self, keyboard: InlineKeyboardBuilder, name: str, state: FSMContext, page_size: int = 5,
                 pre: InlineKeyboardBuilder | None = None, post: InlineKeyboardBuilder | None = None,
                 text: str | None = None, parse_mode: str = 'HTML'):
        self.keyboard = keyboard
        self.pre = pre
        self.post = post
        self.state = state
        self.page_size = page_size
        self.last_viewed_page = 1
        self.text = text
        self.parse_mode = parse_mode
        self.keyboard_id = name
        self.items = self.keyboard.export()

    def first_page(self) -> InlineKeyboardMarkup:
        """Вернуть Markup для первой страницы. При вызове этого метода объект записывается в состояние как последняя
         открытая клавиатура"""
        rows = self.items[:self.page_size]
        if len(self.items) > self.page_size:
            nav_buttons = self._get_navigation_buttons(page=1)
            rows.append(nav_buttons)
        self._add_static_buttons(rows)
        self.last_viewed_page = 1
        return InlineKeyboardMarkup(inline_keyboard=rows)

    def page(self, page: int) -> InlineKeyboardMarkup:
        """Вернуть Markup для страницы с номером ``page``"""
        i = (page-1) * self.page_size
        rows = self.items[i:i+self.page_size]
        if len(self.items) > self.page_size:
            nav_buttons = self._get_navigation_buttons(page=page)
            rows.append(nav_buttons)
        self._add_static_buttons(rows)
        return InlineKeyboardMarkup(inline_keyboard=rows)

    def last_opened_page_cb(self) -> Page:
        """Вернуть Callback на последнюю открытую страницу клавиатуры"""
        return Page(keyboard_id=self.keyboard_id, page=self.last_viewed_page)

    async def _write_keyboard_to_state(self):
        paginated_keyboards = await self._get_paginated_keyboards()
        paginated_keyboards[self.keyboard_id] = self
        await self.state.update_data(paginated_keyboards=paginated_keyboards)

    async def _get_paginated_keyboards(self) -> dict[str, PaginatedKeyboard]:
        data = await self.state.get_data()
        paginated_keyboards = data.get('paginated_keyboards')
        if not paginated_keyboards:
            paginated_keyboards = {}
        return paginated_keyboards

    def _get_navigation_buttons(self, page: int) -> list[InlineKeyboardButton]:
        previous_button = InlineKeyboardButton(text="⬅️", callback_data=Page(keyboard_id=self.keyboard_id, page=page-1).pack())
        next_button = InlineKeyboardButton(text="➡️", callback_data=Page(keyboard_id=self.keyboard_id, page=page+1).pack())
        nav_stub = InlineKeyboardButton(text='❌', callback_data='none')
        current_page = InlineKeyboardButton(text=f'Страница {page}', callback_data='none')

        last_page_index = page * self.page_size
        if last_page_index >= len(self.items):
            return [previous_button, current_page, nav_stub]
        elif page == 1:
            return [nav_stub, current_page, next_button]
        else:
            return [previous_button, current_page, next_button]

    def _add_static_buttons(self, rows: list[list[InlineKeyboardButton]]):
        if self.pre:
            if buttons := self.pre.export():
                for row in reversed(buttons):
                    rows.insert(0, row)
        if self.post:
            if buttons := self.post.export():
                for row in buttons:
                    rows.append(row)
