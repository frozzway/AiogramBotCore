from functools import partial

from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, relationship, Mapped
from sqlalchemy.orm import mapped_column


__all__ = ["Category", "Button", "LinkButton", "ScenarioButton", "Ownership"]

# Выбрасывать исключение при попытке обратиться к незагруженному свойству (lazy_loading)
relationship = partial(relationship, lazy='raise_on_sql')


class Base(DeclarativeBase):
    pass


class Category(Base):
    """Категория"""
    __tablename__ = 'Categories'
    Id: Mapped[int] = mapped_column(primary_key=True)

    Name: Mapped[str] = mapped_column(comment='Наименование категории (заголовок)')
    Text: Mapped[str] = mapped_column(comment='Текст категории')
    tree_header: Mapped[bool] = mapped_column(default=False, comment='Флаг вывода наименования категории с наименованием родителя')


class Button(Base):
    """Базовый класс для всех элементов, не являющимися категориями"""
    __tablename__ = "Buttons"
    Id: Mapped[int] = mapped_column(primary_key=True)
    Name: Mapped[str]
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


class Ownership(Base):
    """Принадлежность категорий и элементов родительской категории"""
    __tablename__ = 'Ownerships'
    id: Mapped[int] = mapped_column(primary_key=True)

    owner_category_id: Mapped[int] = mapped_column(ForeignKey('Categories.id'), comment='Категория, к которой отнесен элемент')
    category_id: Mapped[int | None] = mapped_column(ForeignKey('Categories.id'), comment='Отнесенная категория')
    button_id: Mapped[int | None] = mapped_column(ForeignKey('Buttons.id'), comment='Отнесенный элемент')
    position: Mapped[int] = mapped_column(comment='Позиция элемента в категории')
