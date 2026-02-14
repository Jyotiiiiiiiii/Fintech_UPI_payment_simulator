from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# User Schemas
class UserCreate(BaseModel):
    name: str
    email: str
    upi_id: str
    phone: str
    initial_balance: float = 1000.0

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    upi_id: str
    phone: str
    balance: float
    created_at: datetime

    class Config:
        from_attributes = True

# Transaction Schemas
class TransactionCreate(BaseModel):
    sender_upi: str
    receiver_upi: str
    amount: float
    description: Optional[str] = None

class TransactionResponse(BaseModel):
    id: int
    sender_id: int
    receiver_id: int
    amount: float
    status: str
    description: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True

# Payment Schemas
class PaymentRequest(BaseModel):
    sender_upi: str
    receiver_upi: str
    amount: float
    description: Optional[str] = None
    pin: str

class PaymentResponse(BaseModel):
    success: bool
    message: str
    transaction_id: Optional[int]
    timestamp: datetime
