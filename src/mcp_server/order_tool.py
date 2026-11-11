
from fastmcp import FastMCP
from pydantic import ValidationError

from src.models.order import OrderCreate, OrderStatus
from src.services.order_services import (
    create_order,
    get_order,
    list_customer_orders,
    update_order_status,
)


def register_order_tools(mcp: FastMCP):
    """Register order management tools with the MCP server."""

    @mcp.tool(name="create_order")
    def create_order_tool(
        customer_id: str,
        items: list[dict],
    ) -> dict:
        """Create an order for an existing customer.

        Accepts a customer ID and a list of products.
        Calculates the total amount automatically.
        Rejects unknown customers and invalid order items.
        """

        try:
            order_data = OrderCreate(
                customer_id=customer_id,
                items=items,
            )

            order = create_order(order_data)

            return {
                "success": True,
                "order": order.model_dump(mode="json"),
            }

        except (ValueError, ValidationError) as error:
            return {
                "success": False,
                "error": str(error),
            }

    @mcp.tool
    def get_order_tool(order_id: str) -> dict:
        """Retrieve an order using its unique order ID."""

        try:
            order = get_order(order_id)

            return {
                "success": True,
                "order": order.model_dump(mode="json"),
            }

        except ValueError as error:
            return {
                "success": False,
                "error": str(error),
            }

    @mcp.tool
    def list_customer_orders_tool(customer_id: str) -> dict:
        """Retrieve all orders associated with a particular customer ID."""

        try:
            orders = list_customer_orders(customer_id)

            return {
                "success": True,
                "orders": [
                    order.model_dump(mode="json")
                    for order in orders
                ],
                "count": len(orders),
            }

        except ValueError as error:
            return {
                "success": False,
                "error": str(error),
            }

    @mcp.tool
    def update_order_status_tool(
        order_id: str,
        new_status: OrderStatus,
    ) -> dict:
        """Update an order status.

        Allowed statuses: pending, confirmed, processing,
        shipped, delivered, cancelled.

        Only valid status transitions are accepted.
        """

        try:
            order = update_order_status(order_id, new_status)

            return {
                "success": True,
                "order": order.model_dump(mode="json"),
            }

        except (ValueError, ValidationError) as error:
            return {
                "success": False,
                "error": str(error),
            }
