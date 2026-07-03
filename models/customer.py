from typing import Literal

from pydantic import BaseModel


CustomerStatus = Literal["lead", "active", "archived"]


class Customer(BaseModel):
    id: int
    name: str
    email: str
    company: str | None
    status: CustomerStatus
    notes: str | None
