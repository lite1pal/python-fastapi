from schemas.customer import (
    CreateCustomerRequest,
    CustomerResponse,
    PatchCustomerRequest,
    Customer,
)
from fastapi import HTTPException

from repositories import customers as customer_repo


# customers: dict[int, Customer] = {}
next_id = 1


def to_response(customer: Customer) -> CustomerResponse:
    return CustomerResponse(**customer.model_dump())


def list(limit: int = 10, search: str | None = None) -> list[CustomerResponse]:
    return []


def get(id: int) -> CustomerResponse:
    customer = customer_repo.get(id)

    if customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")

    return to_response(customer)


def patch(id: int, payload: PatchCustomerRequest) -> CustomerResponse:
    current_customer = customer_repo.get(id)

    if current_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")

    updates = payload.model_dump(exclude_unset=True)
    updated_customer = current_customer.model_copy(update=updates)

    saved_customer = customer_repo.update(id, updated_customer)
    return to_response(saved_customer)


def create(payload: CreateCustomerRequest) -> CustomerResponse:
    global next_id

    for customer in customers.values():
        if customer.email == payload.email:
            raise HTTPException(status_code=400, detail="Email already exists")

    customer = Customer(
        id=next_id,
        name=payload.name,
        email=payload.email,
        company=payload.company,
        status=payload.status,
        notes=payload.notes,
    )

    created_customer = customer_repo.create(customer)

    return to_response(created_customer)


def delete(id: int) -> CustomerResponse:
    current_customer = customer_repo.get(id)

    if current_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")

    archived_customer = current_customer.model_copy(update={"status": "archived"})

    customers[id] = archived_customer

    return to_response(archived_customer)
