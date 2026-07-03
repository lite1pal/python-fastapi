from schemas.customer import (
    CreateCustomerRequest,
    CustomerResponse,
    PatchCustomerRequest,
    CreateCustomerAvatarUploadRequest,
    CustomerAvatarUploadResponse,
)
from models.customer import Customer
from fastapi import HTTPException

from repositories import customers as customer_repo

from providers.ai import AIProvider, FakeAIProvider
from providers.storage import FakeR2StorageProvider, StorageProvider

ai_provider: AIProvider = FakeAIProvider()
storage_provider: StorageProvider = FakeR2StorageProvider()


def to_response(customer: Customer) -> CustomerResponse:
    return CustomerResponse(**customer.model_dump())


def list(
    limit: int = 10,
    search: str | None = None,
) -> list[CustomerResponse]:
    customers = customer_repo.list_customers()

    if search is not None:
        search_lower = search.lower()
        customers = [
            customer
            for customer in customers
            if search_lower in customer.name.lower()
            or search_lower in customer.email.lower()
            or (
                customer.company is not None
                and search_lower in customer.company.lower()
            )
        ]

    return [to_response(customer) for customer in customers[:limit]]


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
    existing_customer = customer_repo.get_by_email(payload.email)

    if existing_customer is not None:
        raise HTTPException(status_code=400, detail="Email already exists")

    customer = Customer(
        id=0,
        name=payload.name,
        email=payload.email,
        company=payload.company,
        status=payload.status,
        notes=payload.notes,
    )

    created_customer = customer_repo.create(customer)

    return to_response(created_customer)


def delete(customer_id: int) -> CustomerResponse:
    archived_customer = customer_repo.archive_customer(customer_id)

    if archived_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")

    return to_response(archived_customer)


def summarize_customer_notes(id: int) -> str:
    customer = customer_repo.get_by_id(id)

    if customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")

    if customer.notes is None:
        raise HTTPException(status_code=400, detail="Customer has no notes")

    return ai_provider.summarize(customer.notes)


def create_customer_avatar_upload_url(
    id: int, payload: CreateCustomerAvatarUploadRequest
) -> dict[str, str]:
    customer = customer_repo.get_by_id(id)

    if customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")

    presigned_upload = storage_provider.create_presigned_upload_url(
        filename=payload.filename, content_type=payload.content_type
    )

    return CustomerAvatarUploadResponse(**presigned_upload.model_dump())
