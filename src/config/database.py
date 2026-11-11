
import json
from pathlib import Path

# Project root directory
BASE_DIR = Path(__file__).resolve().parents[2]

# Data directory
DATA_DIR = BASE_DIR / "data"

# JSON file paths
CUSTOMERS_FILE = DATA_DIR / "customers.json"
ORDERS_FILE = DATA_DIR / "orders.json"


def initialize_database():
    """Create data directory and JSON files if they don't exist."""

    DATA_DIR.mkdir(parents=True, exist_ok=True)

    for file_path in [CUSTOMERS_FILE, ORDERS_FILE]:
        if not file_path.exists():
            file_path.write_text("[]", encoding="utf-8")


def read_json(file_path: Path) -> list:
    """Read records from a JSON file."""

    initialize_database()

    with file_path.open("r", encoding="utf-8") as file:
        return json.load(file)


def write_json(file_path: Path, data: list):
    """Write records to a JSON file."""

    initialize_database()

    with file_path.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)
