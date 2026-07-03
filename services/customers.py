from schemas.customer import (
    CreateCustomerRequest,
    CustomerResponse,
    PatchCustomerRequest,
    CreateCustomerAvatarUploadRequest,
    CustomerAvatarUploadResponse,
)
from models.customer import Customer
from fastapi import HTTPException
from sqlalchemy.orm import Session

from repositories import customers as customer_repo

from providers.ai import AIProvider, FakeAIProvider
from providers.storage import FakeR2StorageProvider, StorageProvider
from providers.email import FakeEmailProvider, EmailProvider

ai_provider: AIProvider = FakeAIProvider()
storage_provider: StorageProvider = FakeR2StorageProvider()
email_provider: EmailProvider = FakeEmailProvider()


def to_response(customer: Customer) -> CustomerResponse:
    return CustomerResponse.model_validate(customer)


def list(
    db: Session,
    limit: int = 10,
    search: str | None = None,
) -> list[CustomerResponse]:
    customers = customer_repo.list_customers(db)

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


def get(db: Session, id: int) -> CustomerResponse:
    customer = customer_repo.get(db, id)

    if customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")

    return to_response(customer)


def patch(db: Session, id: int, payload: PatchCustomerRequest) -> CustomerResponse:
    current_customer = customer_repo.get(db, id)

    if current_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")

    updates = payload.model_dump(exclude_unset=True)
    for field, value in updates.items():
        setattr(current_customer, field, value)

    saved_customer = customer_repo.update(db, current_customer)
    return to_response(saved_customer)


def create(db: Session, payload: CreateCustomerRequest) -> CustomerResponse:
    existing_customer = customer_repo.get_by_email(db, payload.email)

    if existing_customer is not None:
        raise HTTPException(status_code=400, detail="Email already exists")

    customer = Customer(
        name=payload.name,
        email=payload.email,
        company=payload.company,
        status=payload.status,
        notes=payload.notes,
    )

    created_customer = customer_repo.create(db, customer)

    email_provider.send_customer_created(
        to_email=created_customer.email,
        customer_name=created_customer.name,
        company=created_customer.company,
    )

    return to_response(created_customer)


def delete(db: Session, customer_id: int) -> CustomerResponse:
    archived_customer = customer_repo.archive_customer(db, customer_id)

    if archived_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")

    return to_response(archived_customer)


def summarize_customer_notes(db: Session, id: int) -> str:
    customer = customer_repo.get_by_id(db, id)

    if customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")

    if customer.notes is None:
        raise HTTPException(status_code=400, detail="Customer has no notes")

    return ai_provider.summarize(customer.notes)


def create_customer_avatar_upload_url(
    db: Session, id: int, payload: CreateCustomerAvatarUploadRequest
) -> dict[str, str]:
    customer = customer_repo.get_by_id(db, id)

    if customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")

    presigned_upload = storage_provider.create_presigned_upload_url(
        filename=payload.filename, content_type=payload.content_type
    )

    return CustomerAvatarUploadResponse(**presigned_upload.model_dump())
