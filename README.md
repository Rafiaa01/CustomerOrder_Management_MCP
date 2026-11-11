# HR Leave Management MCP Assistant

## Overview
A Python-based HR Leave Management system built using **FastMCP, Model Context Protocol (MCP), and FastAPI**. It provides leave management functionality through MCP tools, resources, and prompts, with a separate HTTP API for testing through Postman.

## Features

- **MCP Server:** Built using FastMCP with STDIO transport.
- **Resource:** Exposes the annual leave policy through `hr://policies/employee-handbook`.
- **Prompt:** `leave_application_assistant` provides reusable instructions for checking policy, verifying leave balance, collecting dates, and requesting confirmation before submission.
- **MCP Tools:**
  - `get_leave_balance` – Check employee leave balance.
  - `apply_leave` – Submit leave applications.
  - `get_pending_leave_requests` – Retrieve pending applications.
  - `review_leave_application` – Approve or reject applications.
- **Validation:** Checks employee IDs, date ranges, available balance, and overlapping leave requests.
- **Data Persistence:** Uses JSON files to store fictional employee records, leave balances, and leave applications.
- **Approval Workflow:** Deducts leave balance only after manager approval.
- **FastAPI Integration:** Provides HTTP endpoints protected by API-key authentication.

## API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/employees/{employee_id}/leave-balance` | Check leave balance |
| POST | `/leave/apply` | Submit leave application |
| GET | `/manager/leave-requests` | View pending requests |
| POST | `/manager/leave-requests/{application_id}/review` | Approve/reject requests |

## Technologies

Python · FastMCP · MCP · FastAPI · Pydantic · JSON · MCP Inspector · Postman

## Setup and Testing

Install dependencies:

```bash
pip install -r requirements.txt
```

Run FastAPI:

```bash
uvicorn application:application --reload
```

API documentation:

`http://127.0.0.1:8000/docs`

Run MCP Inspector:

```bash
fastmcp dev inspector src/mcp_server/server.py
```

Use MCP Inspector to test resources, prompts, and tools, and Postman to test the HTTP endpoints.

## Key Concepts

Tools vs. Resources vs. Prompts · FastMCP decorators · Resource URIs · STDIO transport · MCP Inspector · Input validation · JSON persistence · Leave approval workflows.