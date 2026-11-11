
import sys

from src.models.order import OrderCreate, OrderItem, OrderStatus
from src.services.customer_service import list_customers
from src.services.order_services import (
    create_order,
    get_order,
    list_customer_orders,
    update_order_status,
)

# Get an existing customer
customers = list_customers()

if not customers:
    print("Create a customer first.")
    sys.exit()

customer = customers[0]

# Create an order
order_data = OrderCreate(
    customer_id=customer.customer_id,
    items=[
        OrderItem(
            product_name="Laptop",
            quantity=1,
            price=120000,
        ),
        OrderItem(
            product_name="Mouse",
            quantity=2,
            price=1500,
        ),
    ],
)

order = create_order(order_data)

print("Created order:", order.model_dump(mode="json"))
print("Total:", order.total_amount)

# Retrieve order
print("Retrieved:", get_order(order.order_id))

# List customer orders
print("Customer orders:", list_customer_orders(customer.customer_id))

# Update status
updated = update_order_status(
    order.order_id,
    OrderStatus.CONFIRMED,
)

print("Updated status:", updated.status.value)
