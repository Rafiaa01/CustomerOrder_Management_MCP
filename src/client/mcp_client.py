import asyncio
import json

from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client

MCP_SERVER_URL = "http://127.0.0.1:8001/mcp"


def ask(prompt):
    """Read input; return None if the user pressed Ctrl+C or input was closed."""
    try:
        return input(prompt)
    except (EOFError, KeyboardInterrupt):
        return None


def display_result(response):
    """Display successful results and handle MCP tool errors."""

    is_error = getattr(response, "is_error", getattr(response, "isError", False))
    structured_content = getattr(response, "structured_content", None) or getattr(
        response, "structuredContent", None
    )

    if is_error:
        print("\nTool execution failed.")
        for content in response.content:
            if hasattr(content, "text"):
                print(content.text)
        return

    if structured_content:
        if structured_content.get("success") is False:
            print("\nOperation failed:")
            print(structured_content.get("error", "Unknown error"))
        else:
            print("\nOperation successful:")
            print(json.dumps(structured_content, indent=4))
        return

    for content in response.content:
        if hasattr(content, "text"):
            try:
                result = json.loads(content.text)

                if isinstance(result, dict) and result.get("success") is False:
                    print("\nOperation failed:")
                    print(result.get("error", "Unknown error"))
                else:
                    print(json.dumps(result, indent=4))

            except json.JSONDecodeError:
                print(content.text)


async def main():
    try:
        async with (
            streamable_http_client(MCP_SERVER_URL) as (
                read_stream,
                write_stream,
            ),
            ClientSession(read_stream, write_stream) as session,
        ):
            await session.initialize()
            print("\nConnected to MCP server!")

            # Discover tools dynamically
            result = await session.list_tools()
            available_tools = result.tools

            if not available_tools:
                print("No tools are currently available.")
                return

            print("\nAvailable tools:")

            for index, tool in enumerate(available_tools, start=1):
                print(f"{index}. {tool.name}")
                print(f"   {tool.description}")

            # Select a tool
            tool_name = ask("\nEnter tool name: ")
            if tool_name is None:
                print("\nClient stopped.")
                return
            tool_name = tool_name.strip()

            selected_tool = next(
                (tool for tool in available_tools if tool.name == tool_name),
                None,
            )

            if selected_tool is None:
                print("Error: Tool not found. Choose a discovered tool.")
                return

            print("\nInput schema:")
            schema = getattr(selected_tool, "input_schema", None) or getattr(
                selected_tool, "inputSchema", None
            )
            print(json.dumps(schema, indent=4))

            # Collect arguments
            raw_arguments = ask("\nEnter arguments as JSON (use {} if none): ")
            if raw_arguments is None:
                print("\nClient stopped.")
                return
            raw_arguments = raw_arguments.strip() or "{}"

            try:
                arguments = json.loads(raw_arguments)
            except json.JSONDecodeError as error:
                print(f"Invalid JSON: {error}")
                return

            if not isinstance(arguments, dict):
                print("Invalid input: Arguments must be a JSON object.")
                return

            # Invoke the selected tool
            try:
                response = await session.call_tool(
                    tool_name,
                    arguments=arguments,
                )
                display_result(response)

            except Exception as error:  # noqa: BLE001
                print(f"Tool invocation failed: {error}")

    except* (EOFError, KeyboardInterrupt):
        print("\nClient stopped.")

    except* Exception as error_group:  # noqa: BLE001
        print("\nMCP client encountered an error:")

        for error in error_group.exceptions:
            print(f"\nError type: {type(error).__name__}")
            print(f"Error details: {error!r}")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nClient stopped.")
        