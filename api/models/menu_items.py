from sqlalchemy import Column, Integer, String, Float, Text
from sqlalchemy.orm import relationship
from ..dependencies.database import Base


class MenuItem(Base):
    __tablename__ = "menu_items"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False, unique=True)
    category = Column(String(50), nullable=False)
    ingredients = Column(Text, nullable=True)
    calories = Column(Integer, nullable=True)
    price = Column(Float, nullable=False)

    order_items = relationship("OrderItem", back_populates="menu_item")
    reviews = relationship("Review", back_populates="menu_item")
