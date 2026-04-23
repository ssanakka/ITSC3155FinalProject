from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from api.models.orders import OrderType, OrderStatus
from api.schemas.order_items import OrderItem


class OrderBase(BaseModel):
    customer_id: int
    order_type: OrderType
    promo_code: Optional[str] = None


class OrderCreate(OrderBase):
    pass


class OrderUpdate(BaseModel):
    order_type: Optional[OrderType] = None
    status: Optional[OrderStatus] = None
    promo_code: Optional[str] = None
    total_price: Optional[float] = None


class Order(OrderBase):
    id: int
    status: OrderStatus
    tracking_number: str
    total_price: float
    created_at: Optional[datetime] = None
    order_items: list[OrderItem] = []

    class ConfigDict:
        from_attributes = True
