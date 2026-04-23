from pydantic import BaseModel
from typing import Optional
from api.schemas.menu_items import MenuItem


class OrderItemBase(BaseModel):
    order_id: int
    menu_item_id: int
    quantity: int
    price: float


class OrderItemCreate(OrderItemBase):
    pass


class OrderItemUpdate(BaseModel):
    quantity: Optional[int] = None
    price: Optional[float] = None


class OrderItem(OrderItemBase):
    id: int
    menu_item: Optional[MenuItem] = None

    class ConfigDict:
        from_attributes = True
