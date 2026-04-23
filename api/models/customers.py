from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from ..dependencies.database import Base


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    phone = Column(String(20), nullable=False)
    address = Column(String(255), nullable=False)
    email = Column(String(100), unique=True, nullable=True)

    orders = relationship("Order", back_populates="customer")
    payments = relationship("Payment", back_populates="customer")
    reviews = relationship("Review", back_populates="customer")
