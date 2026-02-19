from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
from app.database.config import get_db
from app.database.models import User, Transaction, TransactionStatus
from app.models.schemas import PaymentRequest, PaymentResponse, TransactionResponse
from app.utils.email_service import send_transaction_notification

router = APIRouter(prefix="/api/payments", tags=["payments"])

@router.post("/send", response_model=PaymentResponse)
def send_payment(payment: PaymentRequest, db: Session = Depends(get_db)):
    """Process UPI payment between two users"""
    
    # Get sender
    sender = db.query(User).filter(User.upi_id == payment.sender_upi).first()
    if not sender:
        return PaymentResponse(
            success=False,
            message="Sender not found",
            transaction_id=None,
            timestamp=datetime.utcnow()
        )
    
    # Get receiver
    receiver = db.query(User).filter(User.upi_id == payment.receiver_upi).first()
    if not receiver:
        return PaymentResponse(
            success=False,
            message="Receiver not found",
            transaction_id=None,
            timestamp=datetime.utcnow()
        )
    
    # Verify PIN
    if payment.pin != sender.pin:
        return PaymentResponse(
            success=False,
            message="Invalid PIN",
            transaction_id=None,
            timestamp=datetime.utcnow()
        )
    
    # Check balance
    if sender.balance < payment.amount:
        return PaymentResponse(
            success=False,
            message="Insufficient balance",
            transaction_id=None,
            timestamp=datetime.utcnow()
        )
    
    # Validate amount
    if payment.amount <= 0:
        return PaymentResponse(
            success=False,
            message="Amount must be greater than 0",
            transaction_id=None,
            timestamp=datetime.utcnow()
        )
    
    # Process payment
    try:
        # Create transaction record
        transaction = Transaction(
            sender_id=sender.id,
            receiver_id=receiver.id,
            amount=payment.amount,
            description=payment.description,
            status=TransactionStatus.SUCCESS
        )
        
        # Update balances
        sender.balance -= payment.amount
        receiver.balance += payment.amount
        
        db.add(transaction)
        db.commit()
        db.refresh(transaction)
        
        # Send email notifications to both sender and receiver
        try:
            send_transaction_notification(
                sender_email=sender.email,
                sender_name=sender.name,
                receiver_email=receiver.email,
                receiver_name=receiver.name,
                amount=payment.amount,
                transaction_id=transaction.id,
                description=payment.description,
                timestamp=transaction.created_at
            )
        except Exception as email_error:
            print(f"Email notification failed: {str(email_error)}")
        
        return PaymentResponse(
            success=True,
            message=f"Payment of {payment.amount} sent successfully to {payment.receiver_upi}",
            transaction_id=transaction.id,
            timestamp=datetime.utcnow()
        )
    
    except Exception as e:
        db.rollback()
        return PaymentResponse(
            success=False,
            message=f"Payment failed: {str(e)}",
            transaction_id=None,
            timestamp=datetime.utcnow()
        )

@router.get("/transactions/{upi_id}", response_model=list[TransactionResponse])
def get_user_transactions(upi_id: str, db: Session = Depends(get_db)):
    """Get all transactions for a user"""
    
    user = db.query(User).filter(User.upi_id == upi_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    transactions = db.query(Transaction).filter(
        (Transaction.sender_id == user.id) | (Transaction.receiver_id == user.id)
    ).order_by(Transaction.created_at.desc()).all()
    
    return transactions

@router.get("/transaction/{transaction_id}", response_model=TransactionResponse)
def get_transaction_details(transaction_id: int, db: Session = Depends(get_db)):
    """Get transaction details by ID"""
    
    transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found"
        )
    
    return transaction

@router.get("/all-transactions", response_model=list[TransactionResponse])
def get_all_transactions(db: Session = Depends(get_db)):
    """Get all transactions in the system"""
    
    transactions = db.query(Transaction).order_by(Transaction.created_at.desc()).all()
    return transactions
