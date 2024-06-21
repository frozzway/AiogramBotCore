from datetime import datetime
from functools import partial
from typing import Union

from sqlalchemy import ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship, Mapped
from sqlalchemy.orm import mapped_column

from core.database import Base


__all__ = ["Category", "Button", "LinkButton", "ScenarioButton", "Ownership", "Element", "Statistic"]

# Выбрасывать исключение при попытке обратиться к незагруженному свойству (lazy_loading)
relationship = partial(relationship, lazy='raise_on_sql')


class Category(Base):
    """Категория"""
    __tablename__ = 'Categories'
    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(comment='Наименование категории (заголовок)')
    text: Mapped[str | None] = mapped_column(comment='Текст категории')
    tree_header: Mapped[bool] = mapped_column(default=False, comment='Флаг вывода наименования категории с наименованием родителя')
    page_size: Mapped[int | None] = mapped_column(comment='Количество кнопок на одной странице категории (при пагинации)')


class Button(Base):
    """Базовый класс для всех элементов, не являющимися категориями"""
    __tablename__ = "Buttons"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    Discriminator: Mapped[str]

    __mapper_args__ = {
        "polymorphic_abstract": True,
        "polymorphic_on": "Discriminator",
    }


class LinkButton(Button):
    """Кнопка-ссылка на url"""
    url: Mapped[str] = mapped_column(nullable=True)

    __mapper_args__ = {
        "polymorphic_identity": "LinkButton",
    }


class ScenarioButton(Button):
    """Кнопка вызывающая сценарий"""
    callback_url: Mapped[str] = mapped_column(nullable=True)

    __mapper_args__ = {
        "polymorphic_identity": "ScenarioButton",
    }

    def __hash__(self):
        return hash(self.callback_url)

    def __eq__(self, other):
        return isinstance(other, ScenarioButton) and self.callback_url == other.callback_url


class Ownership(Base):
    """Принадлежность категорий и элементов родительской категории"""
    __tablename__ = 'Ownerships'
    id: Mapped[int] = mapped_column(primary_key=True)

    owner_category_id: Mapped[int] = mapped_column(ForeignKey('Categories.id'), comment='Категория, к которой отнесен элемент')
    category_id: Mapped[int | None] = mapped_column(ForeignKey('Categories.id'), comment='Отнесенная категория')
    button_id: Mapped[int | None] = mapped_column(ForeignKey('Buttons.id'), comment='Отнесенный элемент')
    position_x: Mapped[int | None] = mapped_column(comment='Позиция элемента в категории (номер столбца)')
    position_y: Mapped[int] = mapped_column(comment='Позиция элемента в категории (номер строки)')


class Statistic(Base):
    """Статистика посещений категорий"""
    __tablename__ = 'Statistics'
    id: Mapped[int] = mapped_column(primary_key=True)

    category_id: Mapped[int] = mapped_column(ForeignKey('Categories.id'))
    user_id: Mapped[str]
    date: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True))


Element = Union[Category, LinkButton, ScenarioButton]
