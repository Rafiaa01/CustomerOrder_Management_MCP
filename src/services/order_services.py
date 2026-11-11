from src.config.database import (
    CUSTOMERS_FILE,
    ORDERS_FILE,
    read_json,
    write_json,
)
from src.models.order import Order, OrderCreate, OrderStatus

# Allowed order status transitions
STATUS_TRANSITIONS = {
    OrderStatus.PENDING: [
        OrderStatus.CONFIRMED,
        OrderStatus.CANCELLED,
    ],
    OrderStatus.CONFIRMED: [
        OrderStatus.PROCESSING,
        OrderStatus.CANCELLED,
    ],
    OrderStatus.PROCESSING: [
        OrderStatus.SHIPPED,
        OrderStatus.CANCELLED,
    ],
    OrderStatus.SHIPPED: [
        OrderStatus.DELIVERED,
    ],
    OrderStatus.DELIVERED: [],
    OrderStatus.CANCELLED: [],
}


def create_order(order_data: OrderCreate) -> Order:
    """Create an order for an existing customer."""

    customers = read_json(CUSTOMERS_FILE)

    # Verify customer exists
    customer_exists = any(
        customer["customer_id"] == order_data.customer_id for customer in customers
    )

    if not customer_exists:
        raise ValueError("Customer not found.")

    orders = read_json(ORDERS_FILE)

    # Calculate total amount
    total_amount = sum(item.quantity * item.price for item in order_data.items)

    # Create order
    new_order = Order(
        customer_id=order_data.customer_id,
        items=order_data.items,
        total_amount=total_amount,
    )

    # Save order
    orders.append(new_order.model_dump(mode="json"))
    write_json(ORDERS_FILE, orders)

    return new_order


def get_order(order_id: str) -> Order:
    """Retrieve an order using its ID."""

    orders = read_json(ORDERS_FILE)

    for order in orders:
        if order["order_id"] == order_id:
            return Order(**order)

    raise ValueError("Order not found.")


def list_customer_orders(customer_id: str) -> list[Order]:
    """Retrieve all orders belonging to a customer."""

    customers = read_json(CUSTOMERS_FILE)

    if not any(customer["customer_id"] == customer_id for customer in customers):
        raise ValueError("Customer not found.")

    orders = read_json(ORDERS_FILE)

    customer_orders = [
        Order(**order) for order in orders if order["customer_id"] == customer_id
    ]

    return customer_orders


def update_order_status(
    order_id: str,
    new_status: OrderStatus,
) -> Order:
    """Update an order status if the transition is valid."""

    orders = read_json(ORDERS_FILE)

    for order in orders:
        if order["order_id"] == order_id:
            current_status = OrderStatus(order["status"])

            # Check whether transition is allowed
            allowed_statuses = STATUS_TRANSITIONS[current_status]

            if new_status not in allowed_statuses:
                raise ValueError(
                    f"Cannot change status from "
                    f"{current_status.value} to {new_status.value}."
                )

            order["status"] = new_status.value

            write_json(ORDERS_FILE, orders)

            return Order(**order)

    raise ValueError("Order not found.")
