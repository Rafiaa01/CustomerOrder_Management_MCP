from enum import Enum
from uuid import uuid4

from pydantic import BaseModel, Field


class OrderStatus(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


class OrderItem(BaseModel):
    product_name: str = Field(min_length=1)
    quantity: int = Field(gt=0)
    price: float = Field(gt=0)


class OrderCreate(BaseModel):
    customer_id: str
    items: list[OrderItem] = Field(min_length=1)


class Order(BaseModel):
    order_id: str = Field(default_factory=lambda: str(uuid4()))
    customer_id: str
    items: list[OrderItem]
    total_amount: float
    status: OrderStatus = OrderStatus.PENDING
