from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.managers._DbBaseManager import DbBaseManager
from core.tables import *
from core.settings import timezone


class StatisticsManager(DbBaseManager):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session=session)

    async def save_category_visit(self, category_id: int, user_id: str):
        """Сохранить запись о посещении категории пользователем, если такой записи в день вызова не было"""
        if not await self._get_today_category_visit(category_id, user_id):
            visit = Statistic(category_id=category_id, user_id=user_id, date=datetime.now(tz=timezone))
            self.session.add(visit)
            await self.session.commit()

    async def _get_today_category_visit(self, category_id: int, user_id: str) -> Statistic | None:
        """Получить запись о посещении категории пользователем с идентификатором ``user_id`` в день вызова"""
        today = datetime.now(tz=timezone).replace(hour=0, minute=0, second=0, microsecond=0)
        stmt = select(Statistic) \
            .where(Statistic.category_id == category_id, Statistic.user_id == user_id) \
            .where(Statistic.date >= today)
        return await self.session.scalar(stmt)

