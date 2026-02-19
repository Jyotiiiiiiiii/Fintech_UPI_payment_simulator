from datetime import datetime
import enum

class TransactionStatus(str, enum.Enum):
    PENDING = "pending"
    SUCCESS = "success"
    FAILED = "failed"
    CANCELLED = "cancelled"

# Collection Names
USERS_COLLECTION = "users"
TRANSACTIONS_COLLECTION = "transactions"
