from sqlalchemy import select
from sqlalchemy.orm import Session

from models.customer import Customer


def _seed_customers() -> list[Customer]:
    return [
        Customer(
            id=1,
            name="Maya Chen",
            email="maya.chen@northstar.io",
            company="Northstar Labs",
            status="active",
            notes="Interested in annual billing and wants onboarding support for a small ops team.",
        ),
        Customer(
            id=2,
            name="Jordan Alvarez",
            email="jordan@canvaspeak.com",
            company="Canvas Peak",
            status="lead",
            notes="Requested a product demo after seeing the API integration example.",
        ),
        Customer(
            id=3,
            name="Priya Raman",
            email="priya@signalforge.dev",
            company="SignalForge",
            status="archived",
            notes="Churned after a pilot due to timing, but worth re-engaging next quarter.",
        ),
    ]


def seed_customers(db: Session) -> None:
    existing = db.scalar(select(Customer.id).limit(1))
    if existing is not None:
        return

    db.add_all(_seed_customers())
    db.commit()


def list_customers(db: Session) -> list[Customer]:
    return db.scalars(select(Customer).order_by(Customer.id)).all()


def get(db: Session, id: int) -> Customer | None:
    return db.get(Customer, id)


def get_by_id(db: Session, customer_id: int) -> Customer | None:
    return db.get(Customer, customer_id)


def get_by_email(db: Session, email: str) -> Customer | None:
    return db.scalar(select(Customer).where(Customer.email == email))


def update(db: Session, customer: Customer) -> Customer:
    db.add(customer)
    db.commit()
    db.refresh(customer)
    return customer


def create(db: Session, customer: Customer) -> Customer:
    db.add(customer)
    db.commit()
    db.refresh(customer)
    return customer


def archive_customer(db: Session, customer_id: int) -> Customer | None:
    customer = db.get(Customer, customer_id)

    if customer is None:
        return None

    customer.status = "archived"
    db.commit()
    db.refresh(customer)
    return customer
