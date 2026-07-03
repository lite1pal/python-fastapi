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


class CustomerResponse(Customer):
    pass


class CreateCustomerRequest(BaseModel):
    name: str
    email: str
    company: str | None = None
    status: CustomerStatus
    notes: str | None = None


class PatchCustomerRequest(BaseModel):
    name: str | None = None
    email: str | None = None
    company: str | None = None
    status: CustomerStatus | None = None
    notes: str | None = None
