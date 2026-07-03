from fastapi import APIRouter
from schemas.customer import (
    CustomerResponse,
    CreateCustomerRequest,
    PatchCustomerRequest,
    CreateCustomerAvatarUploadRequest,
    CustomerAvatarUploadResponse,
)
from services import customers

router = APIRouter(prefix="/customers", tags=["customers"])


@router.get("", response_model=list[CustomerResponse])
def list_customers(limit: int = 10, search: str | None = None):
    return customers.list(limit=limit, search=search)


@router.get("/{customer_id}", response_model=CustomerResponse)
def get_customer(customer_id: int):
    return customers.get(customer_id)


@router.patch("/{customer_id}", response_model=CustomerResponse)
def patch_customer(customer_id: int, payload: PatchCustomerRequest):
    return customers.patch(customer_id, payload)


@router.post("", response_model=CustomerResponse)
def create_customer(payload: CreateCustomerRequest):
    return customers.create(payload)


@router.post("/{customer_id}/summarize_notes")
def summarize_customer_notes(customer_id: int):
    summary = customers.summarize_customer_notes(customer_id)
    return {"summary": summary}


@router.post("/{customer_id}/upload_url", response_model=CustomerAvatarUploadResponse)
def create_customer_avatar_upload_url(
    customer_id: int, payload: CreateCustomerAvatarUploadRequest
):
    return customers.create_customer_avatar_upload_url(customer_id, payload)


@router.delete("/{customer_id}", response_model=bool)
def delete_customer(customer_id: int):
    return customers.delete(customer_id)
