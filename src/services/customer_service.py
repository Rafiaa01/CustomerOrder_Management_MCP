from src.config.database import (
    CUSTOMERS_FILE,
    read_json,
    write_json,
)
from src.models.customer import Customer, CustomerCreate


def create_customer(customer_data: CustomerCreate) -> Customer:
    """Create a customer and save it to JSON."""

    customers = read_json(CUSTOMERS_FILE)

    # Check for duplicate email
    for customer in customers:
        if customer["email"].lower() == customer_data.email.lower():
            raise ValueError("A customer with this email already exists.")

    # Create customer with a unique ID
    new_customer = Customer(**customer_data.model_dump())

    # Save customer
    customers.append(new_customer.model_dump(mode="json"))
    write_json(CUSTOMERS_FILE, customers)

    return new_customer


def get_customer(customer_id: str) -> Customer:
    """Retrieve a customer using their ID."""

    customers = read_json(CUSTOMERS_FILE)

    for customer in customers:
        if customer["customer_id"] == customer_id:
            return Customer(**customer)

    raise ValueError("Customer not found.")


def list_customers() -> list[Customer]:
    """Retrieve all registered customers."""

    customers = read_json(CUSTOMERS_FILE)

    return [Customer(**customer) for customer in customers]
