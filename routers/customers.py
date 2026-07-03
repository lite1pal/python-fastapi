from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db import get_db
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
def list_customers(
    limit: int = 10, search: str | None = None, db: Session = Depends(get_db)
):
    return customers.list(db=db, limit=limit, search=search)


@router.get("/{customer_id}", response_model=CustomerResponse)
def get_customer(customer_id: int, db: Session = Depends(get_db)):
    return customers.get(db, customer_id)


@router.patch("/{customer_id}", response_model=CustomerResponse)
def patch_customer(
    customer_id: int, payload: PatchCustomerRequest, db: Session = Depends(get_db)
):
    return customers.patch(db, customer_id, payload)


@router.post("", response_model=CustomerResponse)
def create_customer(payload: CreateCustomerRequest, db: Session = Depends(get_db)):
    return customers.create(db, payload)


@router.post("/{customer_id}/summarize_notes")
def summarize_customer_notes(customer_id: int, db: Session = Depends(get_db)):
    return customers.summarize_customer_notes(db, customer_id)


@router.post("/{customer_id}/upload_url", response_model=CustomerAvatarUploadResponse)
def create_customer_avatar_upload_url(
    customer_id: int,
    payload: CreateCustomerAvatarUploadRequest,
    db: Session = Depends(get_db),
):
    return customers.create_customer_avatar_upload_url(db, customer_id, payload)


@router.delete("/{customer_id}", response_model=CustomerResponse)
def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    return customers.delete(db, customer_id)
