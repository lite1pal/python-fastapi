import logging

from sqlalchemy.orm import Session

from errors import (
    ConflictError,
    NotFoundError,
    UpstreamBadGatewayError,
    UpstreamUnavailableError,
    ValidationError,
)
from schemas.customer import (
    CreateCustomerRequest,
    CustomerResponse,
    PatchCustomerRequest,
    CreateCustomerAvatarUploadRequest,
    CustomerAvatarUploadResponse,
    QueuedResponse,
)
from models.customer import Customer

from repositories import customers as customer_repo

from providers.ai import AIProvider, FakeAIProvider
from providers.storage import FakeR2StorageProvider, StorageProvider
from providers.email import FakeEmailProvider, EmailProvider
from providers.queue import FakeQueueProvider, QueueProvider
from providers.analytics import FakeAnalyticsProvider, AnalyticsProvider
from services.side_effects import log_side_effect_failure

ai_provider: AIProvider = FakeAIProvider()
storage_provider: StorageProvider = FakeR2StorageProvider()
email_provider: EmailProvider = FakeEmailProvider()
queue_provider: QueueProvider = FakeQueueProvider()
analytics_provider: AnalyticsProvider = FakeAnalyticsProvider()
logger = logging.getLogger(__name__)


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
        raise NotFoundError("Customer not found")

    return to_response(customer)


def patch(db: Session, id: int, payload: PatchCustomerRequest) -> CustomerResponse:
    current_customer = customer_repo.get(db, id)

    if current_customer is None:
        raise NotFoundError("Customer not found")

    updates = payload.model_dump(exclude_unset=True)
    for field, value in updates.items():
        setattr(current_customer, field, value)

    saved_customer = customer_repo.update(db, current_customer)
    return to_response(saved_customer)


def create(db: Session, payload: CreateCustomerRequest) -> CustomerResponse:
    existing_customer = customer_repo.get_by_email(db, payload.email)

    if existing_customer is not None:
        raise ConflictError("Email already exists")

    customer = Customer(
        name=payload.name,
        email=payload.email,
        company=payload.company,
        status=payload.status,
        notes=payload.notes,
    )

    created_customer = customer_repo.create(db, customer)

    try:
        email_provider.send_customer_created(
            to_email=created_customer.email,
            customer_name=created_customer.name,
            company=created_customer.company,
        )
    except Exception as exc:
        log_side_effect_failure(
            logger,
            "send_customer_created_email",
            exc,
            customer_id=created_customer.id,
            email=created_customer.email,
        )

    try:
        analytics_provider.track_customer_created(
            customer_id=created_customer.id,
            email=created_customer.email,
            status=created_customer.status,
        )
    except Exception as exc:
        log_side_effect_failure(
            logger,
            "track_customer_created",
            exc,
            customer_id=created_customer.id,
        )

    return to_response(created_customer)


def delete(db: Session, customer_id: int) -> CustomerResponse:
    archived_customer = customer_repo.archive_customer(db, customer_id)

    if archived_customer is None:
        raise NotFoundError("Customer not found")

    try:
        analytics_provider.track_customer_archived(customer_id=customer_id)
    except Exception as exc:
        log_side_effect_failure(
            logger,
            "track_customer_archived",
            exc,
            customer_id=customer_id,
        )

    return to_response(archived_customer)


def summarize_customer_notes(db: Session, id: int) -> QueuedResponse:
    customer = customer_repo.get_by_id(db, id)

    if customer is None:
        raise NotFoundError("Customer not found")

    if customer.notes is None:
        raise ValidationError("Customer has no notes")

    try:
        queue_provider.enqueue_customer_notes_summary(customer_id=customer.id)
    except Exception as exc:
        log_side_effect_failure(
            logger,
            "enqueue_customer_notes_summary",
            exc,
            customer_id=customer.id,
        )
        raise UpstreamUnavailableError(
            "Unable to queue notes summary right now",
        ) from exc

    try:
        analytics_provider.track_customer_notes_summary_requested(
            customer_id=customer.id,
        )
    except Exception as exc:
        log_side_effect_failure(
            logger,
            "track_customer_notes_summary_requested",
            exc,
            customer_id=customer.id,
        )

    return QueuedResponse(status="queued")


def create_customer_avatar_upload_url(
    db: Session, id: int, payload: CreateCustomerAvatarUploadRequest
) -> dict[str, str]:
    customer = customer_repo.get_by_id(db, id)

    if customer is None:
        raise NotFoundError("Customer not found")

    try:
        presigned_upload = storage_provider.create_presigned_upload_url(
            filename=payload.filename, content_type=payload.content_type
        )
    except Exception as exc:
        log_side_effect_failure(
            logger,
            "create_presigned_upload_url",
            exc,
            customer_id=customer.id,
            filename=payload.filename,
        )
        raise UpstreamBadGatewayError(
            "Unable to create upload URL right now",
        ) from exc

    return CustomerAvatarUploadResponse(**presigned_upload.model_dump())
