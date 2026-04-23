from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from api.models.payments import PaymentMethod, PaymentStatus


class PaymentBase(BaseModel):
    order_id: int
    customer_id: int
    payment_method: PaymentMethod
    amount: float


class PaymentCreate(PaymentBase):
    pass


class PaymentUpdate(BaseModel):
    payment_method: Optional[PaymentMethod] = None
    payment_status: Optional[PaymentStatus] = None
    amount: Optional[float] = None


class Payment(PaymentBase):
    id: int
    payment_status: PaymentStatus
    created_at: Optional[datetime] = None

    class ConfigDict:
        from_attributes = True
