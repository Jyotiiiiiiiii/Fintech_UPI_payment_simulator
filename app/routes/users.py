from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.config import get_db
from app.database.models import User
from app.models.schemas import UserCreate, UserResponse

router = APIRouter(prefix="/api/users", tags=["users"])

@router.post("/register", response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    """Register a new UPI user"""
    
    # Check if user already exists
    existing_user = db.query(User).filter(
        (User.email == user.email) | (User.upi_id == user.upi_id)
    ).first()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email or UPI ID already exists"
        )
    
    # Create new user
    db_user = User(
        name=user.name,
        email=user.email,
        upi_id=user.upi_id,
        phone=user.phone,
        balance=user.initial_balance
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user

@router.get("/{upi_id}", response_model=UserResponse)
def get_user_by_upi(upi_id: str, db: Session = Depends(get_db)):
    """Get user details by UPI ID"""
    
    user = db.query(User).filter(User.upi_id == upi_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return user

@router.get("/", response_model=list[UserResponse])
def get_all_users(db: Session = Depends(get_db)):
    """Get all registered users"""
    
    users = db.query(User).all()
    return users

@router.get("/user/{user_id}", response_model=UserResponse)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    """Get user details by ID"""
    
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return user

@router.get("/balance/{upi_id}")
def check_balance(upi_id: str, db: Session = Depends(get_db)):
    """Check user balance"""
    
    user = db.query(User).filter(User.upi_id == upi_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return {"upi_id": upi_id, "balance": user.balance}
