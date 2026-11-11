
import asyncio

from fastmcp import FastMCP

from src.config.database import initialize_database
from src.mcp_server.customer_tool import register_customer_tools
from src.mcp_server.order_tool import register_order_tools

# Initialize FastMCP server
mcp = FastMCP("Customer and Order Management Server")


# Initialize JSON storage
initialize_database()


# Register customer and order tools
register_customer_tools(mcp)
register_order_tools(mcp)


if __name__ == "__main__":
    try:
        mcp.run(
            transport="http",
            host="127.0.0.1",
            port=8001,
        )
    except (KeyboardInterrupt, asyncio.CancelledError):
        print("\nServer stopped.")