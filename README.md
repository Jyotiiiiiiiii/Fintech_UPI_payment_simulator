# UPI Payment Simulation System

A comprehensive UPI payment simulation system built with **FastAPI** (backend), **SQLite** (database), and **HTML/CSS/JavaScript** (frontend). This system allows you to simulate real-world UPI transactions including user registration, balance management, and payments.

## 🌟 Features

### Backend
- **User Management**: Register users with unique UPI IDs
- **Balance Management**: Track user balances and check account status
- **Payment Processing**: Send money between users with PIN verification
- **Transaction History**: View all transactions for a user
- **RESTful API**: Complete REST API with automatic documentation
- **SQLite Database**: Persistent data storage

### Frontend
- **Interactive Dashboard**: Beautiful web interface for all operations
- **User Registration**: Easy form to register new users
- **Payment Interface**: Simple way to send payments
- **Transaction Tracking**: View complete transaction history
- **User Management**: See all users and their details
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Real-time Updates**: Instant feedback on all actions

## 📁 Project Structure

```
Fin_UPI/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application entry point
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py          # Pydantic models for request/response
│   ├── database/
│   │   ├── __init__.py
│   │   ├── config.py           # Database configuration
│   │   └── models.py           # SQLAlchemy ORM models
│   └── routes/
│       ├── __init__.py
│       ├── users.py            # User management endpoints
│       └── transactions.py      # Payment endpoints
├── static/
│   ├── index.html              # Main frontend page
│   ├── style.css               # Frontend styling
│   └── script.js               # Frontend JavaScript logic
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables
├── README.md                   # This file
├── FRONTEND_GUIDE.md           # Detailed frontend documentation
├── test_api.py                 # Basic API tests
├── test_api_advanced.py        # Advanced API tests
├── setup_and_run.py            # Automated setup script
├── run_server.bat              # Windows batch script to start server
└── run_server.ps1              # PowerShell script to start server
```

## 🚀 Quick Start
pip install -r requirements.txt

### 2. Run the Application

```bash
python -m uvicorn app.main:app --reload


The API will be available at `http://localhost:8000`

### 3. Access the Documentation

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 💻 Using the Frontend

### Main Features

1. **Dashboard**
   - Search for user by UPI ID
   - View user profile and balance
   - Quick access to user transactions

2. **Register User**
   - Create new user accounts
   - Set initial balance
   - Instant validation and feedback

3. **Send Payment**
   - Simple payment form
   - Sender and receiver selection
   - PIN verification
   - Real-time status updates

4. **Transactions**
   - View transaction history
   - Filter by user
   - See all system transactions
   - Detailed transaction information

5. **All Users**
   - View all registered users
   - User cards with key information
   - Click to see detailed user profile

### Example Usage

1. **Register Users**
   - Go to "Register User" tab
   - Fill in details for first user (e.g., Alice, alice@axis)
   - Register second user (e.g., Bob, bob@axis)

2. **Send Payment**
   - Go to "Send Payment" tab
   - Enter sender UPI ID (alice@axis)
   - Enter receiver UPI ID (bob@axis)
   - Enter amount (e.g., 500)
   - Enter PIN (default: 1234)
   - Click "Send Payment"

3. **Check Transactions**
   - Go to "Transactions" tab
   - Enter UPI ID to filter or click "Show All"
   - View complete transaction details

For detailed frontend guide, see [FRONTEND_GUIDE.md](FRONTEND_GUIDE.md)

## 🔌 API Endpoints

### User Management

- **Register User**: `POST /api/users/register`
  - Register a new UPI user
  - Request body:
    ```json
    {
      "name": "John Doe",
      "email": "john@example.com",
      "upi_id": "john@upi",
      "phone": "9876543210",
      "initial_balance": 5000
    }
    ```

- **Get User by UPI ID**: `GET /api/users/{upi_id}`
  - Retrieve user details using UPI ID

- **Get All Users**: `GET /api/users/`
  - List all registered users

- **Check Balance**: `GET /api/users/balance/{upi_id}`
  - Check account balance for a user

### Payments & Transactions

- **Send Payment**: `POST /api/payments/send`
  - Process a UPI payment between users
  - Request body:
    ```json
    {
      "sender_upi": "john@upi",
      "receiver_upi": "jane@upi",
      "amount": 100,
      "description": "Payment for lunch",
      "pin": "1234"
    }
    ```

- **Get User Transactions**: `GET /api/payments/transactions/{upi_id}`
  - Get all transactions for a specific user

- **Get Transaction Details**: `GET /api/payments/transaction/{transaction_id}`
  - Get details of a specific transaction

- **Get All Transactions**: `GET /api/payments/all-transactions`
  - Get all transactions in the system

## Default Configuration

- **Default User PIN**: `1234`
- **Default Initial Balance**: `1000`
- **Database**: SQLite (auto-created as `upi_system.db`)

## Example Workflow

1. **Register User 1**
   ```bash
   curl -X POST http://localhost:8000/api/users/register \
     -H "Content-Type: application/json" \
     -d '{"name":"Alice","email":"alice@example.com","upi_id":"alice@upi","phone":"9876543210","initial_balance":5000}'
   ```

2. **Register User 2**
   ```bash
   curl -X POST http://localhost:8000/api/users/register \
     -H "Content-Type: application/json" \
     -d '{"name":"Bob","email":"bob@example.com","upi_id":"bob@upi","phone":"9876543211","initial_balance":5000}'
   ```

3. **Send Payment**
   ```bash
   curl -X POST http://localhost:8000/api/payments/send \
     -H "Content-Type: application/json" \
     -d '{"sender_upi":"alice@upi","receiver_upi":"bob@upi","amount":100,"description":"Test payment","pin":"1234"}'
   ```

4. **Check Transaction History**
   ```bash
   curl http://localhost:8000/api/payments/transactions/alice@upi
   ```

## Database Schema

### Users Table
- `id`: Primary key
- `name`: User name
- `email`: Email address (unique)
- `upi_id`: UPI identifier (unique)
- `phone`: Phone number (unique)
- `balance`: Account balance
- `pin`: Security PIN (default: "1234")
- `created_at`: Account creation timestamp

### Transactions Table
- `id`: Primary key
- `sender_id`: Foreign key to sender user
- `receiver_id`: Foreign key to receiver user
- `amount`: Transaction amount
- `status`: Transaction status (pending, success, failed, cancelled)
- `description`: Transaction description
- `created_at`: Transaction timestamp

## Error Handling

The API includes comprehensive error handling:
- `400 Bad Request`: Invalid input or duplicate user
- `404 Not Found`: User or transaction not found
- Payment failures include descriptive error messages:
  - Invalid PIN
  - Insufficient balance
  - Invalid amount
  - User not found

## Security Considerations (Development Only)

This is a simulation system for educational and testing purposes. In production:
- Implement proper encryption for PINs
- Use JWT tokens for authentication
- Add rate limiting
- Implement proper logging and audit trails
- Use HTTPS for all endpoints
- Add input validation and sanitization

## Testing

You can test the API using:
- **Swagger UI**: `http://localhost:8000/docs` (interactive API testing)
- **cURL**: Command-line HTTP client
- **Postman**: REST API testing tool
- **Python requests**: Programmatic API testing

## Future Enhancements

- User authentication with JWT
- Transaction receipts and PDFs
- Bill payment integration
- Merchant integration
- Transaction status tracking
- Refund functionality
- Advanced analytics and reporting
- Mobile app integration

## License

This project is open source and available for educational purposes.

## Support

For issues or questions, please refer to the API documentation at `/docs` endpoint.
