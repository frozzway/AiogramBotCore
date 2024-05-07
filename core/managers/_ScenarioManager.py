from aiogram.filters.callback_data import CallbackData
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.managers._DbBaseManager import DbBaseManager
from core.tables import *
from core.utils import database_call


class ScenarioManager(DbBaseManager):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session=session)

    @database_call
    async def _save_scenarios(self):
        await self.session.commit()

    async def create_scenarios(self, callbacks: dict[str, CallbackData]):
        for scenario_name, callback in callbacks.items():
            callback_url = callback.pack()
            scenario = await self.get_scenario(callback_url)
            if not scenario:
                scenario = ScenarioButton(name=scenario_name)
                self.session.add(scenario)
        await self._save_scenarios()

    @database_call
    async def get_scenario(self, callback_url: str) -> ScenarioButton | None:
        return await self.session.scalar(select(ScenarioButton).where(ScenarioButton.callback_url == callback_url))
