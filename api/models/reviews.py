from sqlalchemy import Column, Integer, String, ForeignKey, Text, DATETIME
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..dependencies.database import Base


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    menu_item_id = Column(Integer, ForeignKey("menu_items.id"), nullable=True)
    rating = Column(Integer, nullable=False)  # 1-5
    comment = Column(Text, nullable=True)
    created_at = Column(DATETIME, nullable=False, server_default=func.now())

    customer = relationship("Customer", back_populates="reviews")
    order = relationship("Order", back_populates="reviews")
    menu_item = relationship("MenuItem", back_populates="reviews")
