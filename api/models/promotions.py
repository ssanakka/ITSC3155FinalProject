from sqlalchemy import Column, Integer, String, Float, Boolean, DATETIME, Date
from sqlalchemy.sql import func
from ..dependencies.database import Base


class Promotion(Base):
    __tablename__ = "promotions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    promo_code = Column(String(50), unique=True, nullable=False)
    description = Column(String(255), nullable=True)
    discount_percent = Column(Float, nullable=False)
    is_active = Column(Boolean, default=True)
    expiration_date = Column(Date, nullable=True)
    created_at = Column(DATETIME, nullable=False, server_default=func.now())
