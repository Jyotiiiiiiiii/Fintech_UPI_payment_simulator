"""
Quick Start Examples for UPI Payment System
Run these commands to test your API
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def print_response(title, response):
    print(f"\n{'='*60}")
    print(f"{title}")
    print(f"{'='*60}")
    print(json.dumps(response.json(), indent=2))

# 1. Register User 1
response = requests.post(f"{BASE_URL}/api/users/register", json={
    "name": "Alice Johnson",
    "email": "alice@example.com",
    "upi_id": "alice@axis",
    "phone": "9876543210",
    "initial_balance": 5000
})
print_response("1. Register User 1 (Alice)", response)

# 2. Register User 2
response = requests.post(f"{BASE_URL}/api/users/register", json={
    "name": "Bob Smith",
    "email": "bob@example.com",
    "upi_id": "bob@axis",
    "phone": "9876543211",
    "initial_balance": 3000
})
print_response("2. Register User 2 (Bob)", response)

# 3. Get user by UPI ID
response = requests.get(f"{BASE_URL}/api/users/alice@axis")
print_response("3. Get User by UPI ID", response)

# 4. Check balance
response = requests.get(f"{BASE_URL}/api/users/balance/alice@axis")
print_response("4. Check Balance", response)

# 5. Send payment
response = requests.post(f"{BASE_URL}/api/payments/send", json={
    "sender_upi": "alice@axis",
    "receiver_upi": "bob@axis",
    "amount": 500,
    "description": "Payment for dinner",
    "pin": "1234"
})
print_response("5. Send Payment (Alice to Bob)", response)

# 6. Check updated balances
response = requests.get(f"{BASE_URL}/api/users/balance/alice@axis")
print(f"\nAlice's updated balance: {response.json()['balance']}")

response = requests.get(f"{BASE_URL}/api/users/balance/bob@axis")
print(f"Bob's updated balance: {response.json()['balance']}")

# 7. Get user transactions
response = requests.get(f"{BASE_URL}/api/payments/transactions/alice@axis")
print_response("7. Get Alice's Transactions", response)

# 8. Get all transactions
response = requests.get(f"{BASE_URL}/api/payments/all-transactions")
print_response("8. Get All Transactions", response)

# 9. Get all users
response = requests.get(f"{BASE_URL}/api/users/")
print_response("9. Get All Users", response)

print("\n" + "="*60)
print("All examples completed successfully!")
print("="*60)
