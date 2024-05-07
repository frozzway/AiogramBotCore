from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.managers._DbBaseManager import DbBaseManager
from core.models.categories import ElementModel
from core.tables import *
from core.utils import database_call


class CategoryManager(DbBaseManager):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session=session)

    @database_call
    async def _create_category(self, category: Category):
        self.session.add(category)
        await self.session.commit()

    async def create_main_category(self):
        category = await self.get_category(1)
        if not category:
            category = Category(name="Главное меню")
            await self._create_category(category)

    @database_call
    async def get_category(self, category_id: int) -> Category | None:
        return await self.session.scalar(select(Category).where(Category.id == category_id))

    @database_call
    async def get_child_categories(self, category_id: int) -> list[ElementModel]:
        """Получить все дочерние категории по идентификатору родительской категории"""
        stmt = select(Category, Ownership.position_x, Ownership.position_y) \
            .select_from(Ownership) \
            .where(Ownership.owner_category_id == category_id) \
            .join(Category, onclause=Category.id == Ownership.category_id) \
            .order_by(Ownership.position_y, Ownership.position_x)

        results = await self.session.execute(stmt)

        return [ElementModel(element=row[0], position_x=row[1], position_y=row[2]) for row in results.all()]

    @database_call
    async def get_child_buttons(self, category_id: int) -> list[ElementModel]:
        """Получить все принадлежащие категории элементы, помимо категорий"""
        stmt = select(Button, Ownership.position_x, Ownership.position_y) \
            .select_from(Ownership) \
            .where(Ownership.owner_category_id == category_id) \
            .join(Button) \
            .order_by(Ownership.position_y, Ownership.position_x)

        results = await self.session.execute(stmt)

        return [ElementModel(element=row[0], position_x=row[1], position_y=row[2]) for row in results.all()]

    async def get_child_elements(self, category_id: int) -> list[list[Element]]:
        """Получить все элементы в категории"""
        elements = []
        elements.extend(await self.get_child_categories(category_id))
        elements.extend(await self.get_child_buttons(category_id))
        sorted_elements = sorted(elements, key=lambda e: (e.position_y, e.position_x))
        return self._group_elements(sorted_elements)

    @staticmethod
    def _group_elements(sorted_elements: list[ElementModel]) -> list[list[Element]]:
        grouped: dict[int, list[Element]] = {}
        for model in sorted_elements:
            if grouped.get(model.position_y) is None:
                grouped[model.position_y] = []
            grouped[model.position_y].append(model.element)

        return [v for v in grouped.values()]
