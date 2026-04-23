from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date


class PromotionBase(BaseModel):
    promo_code: str
    description: Optional[str] = None
    discount_percent: float
    is_active: bool = True
    expiration_date: Optional[date] = None


class PromotionCreate(PromotionBase):
    pass


class PromotionUpdate(BaseModel):
    description: Optional[str] = None
    discount_percent: Optional[float] = None
    is_active: Optional[bool] = None
    expiration_date: Optional[date] = None


class Promotion(PromotionBase):
    id: int
    created_at: Optional[datetime] = None

    class ConfigDict:
        from_attributes = True
