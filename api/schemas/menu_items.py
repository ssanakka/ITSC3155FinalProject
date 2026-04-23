from pydantic import BaseModel
from typing import Optional


class MenuItemBase(BaseModel):
    name: str
    category: str
    ingredients: Optional[str] = None
    calories: Optional[int] = None
    price: float


class MenuItemCreate(MenuItemBase):
    pass


class MenuItemUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    ingredients: Optional[str] = None
    calories: Optional[int] = None
    price: Optional[float] = None


class MenuItem(MenuItemBase):
    id: int

    class ConfigDict:
        from_attributes = True
