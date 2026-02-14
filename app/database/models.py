from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.database.config import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    upi_id = Column(String, unique=True, index=True, nullable=False)
    phone = Column(String, unique=True, nullable=False)
    balance = Column(Float, default=1000.0)
    pin = Column(String, default="1234")  # Default PIN
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relations
    sent_transactions = relationship(
        "Transaction",
        foreign_keys="Transaction.sender_id",
        back_populates="sender"
    )
    received_transactions = relationship(
        "Transaction",
        foreign_keys="Transaction.receiver_id",
        back_populates="receiver"
    )

class TransactionStatus(str, enum.Enum):
    PENDING = "pending"
    SUCCESS = "success"
    FAILED = "failed"
    CANCELLED = "cancelled"

class Transaction(Base):
    __tablename__ = "transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    receiver_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    amount = Column(Float, nullable=False)
    status = Column(Enum(TransactionStatus), default=TransactionStatus.PENDING)
    description = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relations
    sender = relationship(
        "User",
        foreign_keys=[sender_id],
        back_populates="sent_transactions"
    )
    receiver = relationship(
        "User",
        foreign_keys=[receiver_id],
        back_populates="received_transactions"
    )
