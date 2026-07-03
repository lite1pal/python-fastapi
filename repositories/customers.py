from schemas.customer import Customer

# in-memory data
_customers: dict[int, Customer] = {}
_next_id = 1


def get(id: int) -> Customer:
    return _customers.get(id)


def update(id: int, customer: Customer) -> Customer:
    _customers[id] = customer
    return customer


def create(customer: Customer) -> Customer:
    global _next_id

    customer_with_id = customer.model_copy(update={"id": _next_id})

    _customers[_next_id] = customer_with_id
    _next_id += 1

    return customer_with_id
