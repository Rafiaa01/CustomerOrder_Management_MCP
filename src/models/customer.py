
from uuid import uuid4

from pydantic import BaseModel, EmailStr, Field


class CustomerCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    phone: str = Field(min_length=10, max_length=15)


class Customer(BaseModel):
    customer_id: str = Field(
        default_factory=lambda: str(uuid4())
    )
    name: str
    email: EmailStr
    phone: str
