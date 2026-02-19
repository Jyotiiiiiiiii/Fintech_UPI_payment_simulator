from fastapi import APIRouter, Depends, HTTPException, status
from app.database.config import get_db
from app.database.models import USERS_COLLECTION
from app.models.schemas import UserCreate, UserResponse
from datetime import datetime

router = APIRouter(prefix="/api/users", tags=["users"])

@router.post("/register", response_model=UserResponse)
def register_user(user: UserCreate, db = Depends(get_db)):
    """Register a new UPI user"""
    
    # Check if user already exists
    existing_user = db[USERS_COLLECTION].find_one({
        "$or": [
            {"email": user.email},
            {"upi_id": user.upi_id}
        ]
    })
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email or UPI ID already exists"
        )
    
    # Get the next ID (simulating auto-increment)
    last_user = db[USERS_COLLECTION].find_one(sort=[("id", -1)])
    next_id = (last_user["id"] + 1) if last_user else 1
    
    # Create new user
    db_user = {
        "id": next_id,
        "name": user.name,
        "email": user.email,
        "upi_id": user.upi_id,
        "phone": user.phone,
        "balance": user.initial_balance,
        "pin": "1234", # Default PIN
        "created_at": datetime.utcnow()
    }
    
    db[USERS_COLLECTION].insert_one(db_user)
    
    return db_user

@router.get("/{upi_id}", response_model=UserResponse)
def get_user_by_upi(upi_id: str, db = Depends(get_db)):
    """Get user details by UPI ID"""
    
    user = db[USERS_COLLECTION].find_one({"upi_id": upi_id})
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return user

@router.get("/", response_model=list[UserResponse])
def get_all_users(db = Depends(get_db)):
    """Get all registered users"""
    
    users = list(db[USERS_COLLECTION].find())
    return users

@router.get("/user/{user_id}", response_model=UserResponse)
def get_user_by_id(user_id: int, db = Depends(get_db)):
    """Get user details by ID"""
    
    user = db[USERS_COLLECTION].find_one({"id": user_id})
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return user

@router.get("/balance/{upi_id}")
def check_balance(upi_id: str, db = Depends(get_db)):
    """Check user balance"""
    
    user = db[USERS_COLLECTION].find_one({"upi_id": upi_id})
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return {"upi_id": upi_id, "balance": user["balance"]}
