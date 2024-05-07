from pydantic import BaseModel

from core.tables import Element


class ElementModel(BaseModel):
    element: Element
    position_x: int | None
    position_y: int
