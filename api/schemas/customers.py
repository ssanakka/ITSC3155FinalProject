from pydantic import BaseModel
from typing import Optional


class CustomerBase(BaseModel):
    name: str
    phone: str
    address: str
    email: Optional[str] = None


class CustomerCreate(CustomerBase):
    pass


class CustomerUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    email: Optional[str] = None


class Customer(CustomerBase):
    id: int

    class ConfigDict:
        from_attributes = True
