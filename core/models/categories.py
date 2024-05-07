from pydantic import BaseModel, ConfigDict

from core.tables import Element


class ElementModel(BaseModel):
    element: Element
    position_x: int | None
    position_y: int

    model_config = ConfigDict(arbitrary_types_allowed=True)
