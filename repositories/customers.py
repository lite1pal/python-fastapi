from models.customer import Customer


def _seed_customers() -> dict[int, Customer]:
    return {
        1: Customer(
            id=1,
            name="Maya Chen",
            email="maya.chen@northstar.io",
            company="Northstar Labs",
            status="active",
            notes="Interested in annual billing and wants onboarding support for a small ops team.",
        ),
        2: Customer(
            id=2,
            name="Jordan Alvarez",
            email="jordan@canvaspeak.com",
            company="Canvas Peak",
            status="lead",
            notes="Requested a product demo after seeing the API integration example.",
        ),
        3: Customer(
            id=3,
            name="Priya Raman",
            email="priya@signalforge.dev",
            company="SignalForge",
            status="archived",
            notes="Churned after a pilot due to timing, but worth re-engaging next quarter.",
        ),
    }


# In-memory demo data keeps the API useful immediately after startup.
_customers: dict[int, Customer] = _seed_customers()
_next_id = max(_customers) + 1


def list_customers() -> list[Customer]:
    return list(_customers.values())


def get(id: int) -> Customer | None:
    return _customers.get(id)


def get_by_id(customer_id: int) -> Customer | None:
    return _customers.get(customer_id)


def get_by_email(email: str) -> Customer | None:
    for customer in _customers.values():
        if customer.email == email:
            return customer

    return None


def update(id: int, customer: Customer) -> Customer:
    _customers[id] = customer
    return customer


def create(customer: Customer) -> Customer:
    global _next_id

    customer_with_id = customer.model_copy(update={"id": _next_id})

    _customers[_next_id] = customer_with_id
    _next_id += 1

    return customer_with_id


def archive_customer(customer_id: int) -> Customer | None:
    customer = _customers.get(customer_id)

    if customer is None:
        return None

    archived_customer = customer.model_copy(update={"status": "archived"})
    _customers[customer_id] = archived_customer

    return archived_customer
