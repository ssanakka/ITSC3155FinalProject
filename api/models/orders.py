from sqlalchemy import Column, Integer, String, Float, ForeignKey, Enum, DATETIME
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from ..dependencies.database import Base


class OrderType(str, enum.Enum):
    takeout = "takeout"
    delivery = "delivery"


class OrderStatus(str, enum.Enum):
    pending = "pending"
    preparing = "preparing"
    ready = "ready"
    delivered = "delivered"
    cancelled = "cancelled"


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    order_type = Column(Enum(OrderType), nullable=False, default=OrderType.takeout)
    status = Column(Enum(OrderStatus), nullable=False, default=OrderStatus.pending)
    tracking_number = Column(String(20), unique=True, nullable=False)
    total_price = Column(Float, nullable=False, default=0.0)
    promo_code = Column(String(50), nullable=True)
    created_at = Column(DATETIME, nullable=False, server_default=func.now())

    customer = relationship("Customer", back_populates="orders")
    order_items = relationship("OrderItem", back_populates="order", cascade="all, delete")
    payment = relationship("Payment", back_populates="order", uselist=False)
    reviews = relationship("Review", back_populates="order")
