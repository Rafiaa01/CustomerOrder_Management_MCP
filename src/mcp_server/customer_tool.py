
from fastmcp import FastMCP
from pydantic import ValidationError

from src.models.customer import CustomerCreate
from src.services.customer_service import (
    create_customer,
    get_customer,
    list_customers,
)


def register_customer_tools(mcp: FastMCP):
    """Register customer management tools with the MCP server."""

    @mcp.tool(name="create_customer")
    def create_customer_tool(
        name: str,
        email: str,
        phone: str,
    ) -> dict:
        """Register a new store customer using their name, email and phone.

        Rejects duplicate email addresses and invalid customer information.
        """

        try:
            customer_data = CustomerCreate(
                name=name,
                email=email,
                phone=phone,
            )

            customer = create_customer(customer_data)

            return {
                "success": True,
                "customer": customer.model_dump(mode="json"),
            }

        except (ValueError, ValidationError) as error:
            return {
                "success": False,
                "error": str(error),
            }

    @mcp.tool
    def get_customer_tool(customer_id: str) -> dict:
        """Retrieve a store customer using their unique customer ID."""

        try:
            customer = get_customer(customer_id)

            return {
                "success": True,
                "customer": customer.model_dump(mode="json"),
            }

        except ValueError as error:
            return {
                "success": False,
                "error": str(error),
            }

    @mcp.tool
    def list_customers_tool() -> dict:
        """Retrieve all registered store customers."""

        customers = list_customers()

        return {
            "success": True,
            "customers": [
                customer.model_dump(mode="json")
                for customer in customers
            ],
            "count": len(customers),
        }
