from pydantic import BaseModel


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
