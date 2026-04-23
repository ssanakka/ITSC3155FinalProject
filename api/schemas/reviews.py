from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import datetime


class ReviewBase(BaseModel):
    customer_id: int
    order_id: int
    menu_item_id: Optional[int] = None
    rating: int
    comment: Optional[str] = None

    @field_validator("rating")
    @classmethod
    def rating_must_be_1_to_5(cls, v):
        if not 1 <= v <= 5:
            raise ValueError("Rating must be between 1 and 5")
        return v


class ReviewCreate(ReviewBase):
    pass


class ReviewUpdate(BaseModel):
    rating: Optional[int] = None
    comment: Optional[str] = None


class Review(ReviewBase):
    id: int
    created_at: Optional[datetime] = None

    class ConfigDict:
        from_attributes = True
