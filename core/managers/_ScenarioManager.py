from aiogram.filters.callback_data import CallbackData
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.managers._DbBaseManager import DbBaseManager
from core.tables import ScenarioButton
from core.utils import database_call


class ScenarioManager(DbBaseManager):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session=session)

    @database_call
    async def _save_scenarios(self):
        await self.session.commit()

    async def create_scenarios(self, callbacks: dict[str, CallbackData]):
        all_scenarios = await self.get_scenarios()
        for scenario_name, callback in callbacks.items():
            callback_url = callback.pack()
            scenario = ScenarioButton(name=scenario_name, callback_url=callback_url)
            if scenario not in all_scenarios:
                self.session.add(scenario)
        await self._save_scenarios()

    @database_call
    async def get_scenarios(self) -> set[ScenarioButton]:
        result = await self.session.scalars(select(ScenarioButton))
        return set(result)
