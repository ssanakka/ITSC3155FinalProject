from sqlalchemy import Column, Integer, String, Float, ForeignKey, Enum, DATETIME
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from ..dependencies.database import Base


class PaymentMethod(str, enum.Enum):
    credit_card = "credit_card"
    debit_card = "debit_card"
    cash = "cash"
    paypal = "paypal"
    apple_pay = "apple_pay"


class PaymentStatus(str, enum.Enum):
    pending = "pending"
    completed = "completed"
    failed = "failed"
    refunded = "refunded"


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    payment_method = Column(Enum(PaymentMethod), nullable=False)
    payment_status = Column(Enum(PaymentStatus), nullable=False, default=PaymentStatus.pending)
    amount = Column(Float, nullable=False)
    created_at = Column(DATETIME, nullable=False, server_default=func.now())

    order = relationship("Order", back_populates="payment")
    customer = relationship("Customer", back_populates="payments")
