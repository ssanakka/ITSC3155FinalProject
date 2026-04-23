from pydantic import BaseModel
from typing import Optional


class StaffBase(BaseModel):
    name: str
    role: str
    email: str
    phone: Optional[str] = None


class StaffCreate(StaffBase):
    pass


class StaffUpdate(BaseModel):
    name: Optional[str] = None
    role: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None


class Staff(StaffBase):
    id: int

    class ConfigDict:
        from_attributes = True
