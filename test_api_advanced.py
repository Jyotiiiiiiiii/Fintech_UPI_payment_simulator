"""
Advanced Test Cases for UPI Payment System
Tests for error handling and edge cases
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def print_response(title, response, expected_status=200):
    print(f"\n{'='*60}")
    print(f"{title}")
    print(f"Status Code: {response.status_code} (Expected: {expected_status})")
    print(f"{'='*60}")
    try:
        print(json.dumps(response.json(), indent=2))
    except:
        print(response.text)
    print(f"✓ PASS" if response.status_code == expected_status else "✗ FAIL")

print("\n" + "="*60)
print("ADVANCED TEST CASES FOR UPI PAYMENT SYSTEM")
print("="*60)

# Test 1: Duplicate user registration
print("\n[TEST 1] Register duplicate user (should fail)")
response = requests.post(f"{BASE_URL}/api/users/register", json={
    "name": "Alice Johnson",
    "email": "alice@example.com",
    "upi_id": "alice@axis",
    "phone": "9876543210",
    "initial_balance": 5000
})
print_response("Duplicate User Registration", response, 400)

# Test 2: Invalid PIN for payment
print("\n[TEST 2] Send payment with invalid PIN")
response = requests.post(f"{BASE_URL}/api/payments/send", json={
    "sender_upi": "alice@axis",
    "receiver_upi": "bob@axis",
    "amount": 100,
    "description": "Test payment",
    "pin": "9999"  # Wrong PIN
})
print_response("Payment with Invalid PIN", response, 200)

# Test 3: Insufficient balance
print("\n[TEST 3] Send payment with insufficient balance")
response = requests.post(f"{BASE_URL}/api/payments/send", json={
    "sender_upi": "bob@axis",
    "receiver_upi": "alice@axis",
    "amount": 9999999,
    "description": "Large payment",
    "pin": "1234"
})
print_response("Payment with Insufficient Balance", response, 200)

# Test 4: Non-existent user payment
print("\n[TEST 4] Send payment from non-existent user")
response = requests.post(f"{BASE_URL}/api/payments/send", json={
    "sender_upi": "unknown@axis",
    "receiver_upi": "bob@axis",
    "amount": 100,
    "description": "Test",
    "pin": "1234"
})
print_response("Payment from Non-existent User", response, 200)

# Test 5: Get non-existent user
print("\n[TEST 5] Get non-existent user")
response = requests.get(f"{BASE_URL}/api/users/fake@upi")
print_response("Get Non-existent User", response, 404)

# Test 6: Get non-existent transaction
print("\n[TEST 6] Get non-existent transaction")
response = requests.get(f"{BASE_URL}/api/payments/transaction/99999")
print_response("Get Non-existent Transaction", response, 404)

# Test 7: Negative amount payment
print("\n[TEST 7] Send payment with negative amount")
response = requests.post(f"{BASE_URL}/api/payments/send", json={
    "sender_upi": "alice@axis",
    "receiver_upi": "bob@axis",
    "amount": -100,
    "description": "Negative payment",
    "pin": "1234"
})
print_response("Payment with Negative Amount", response, 200)

# Test 8: Zero amount payment
print("\n[TEST 8] Send payment with zero amount")
response = requests.post(f"{BASE_URL}/api/payments/send", json={
    "sender_upi": "alice@axis",
    "receiver_upi": "bob@axis",
    "amount": 0,
    "description": "Zero payment",
    "pin": "1234"
})
print_response("Payment with Zero Amount", response, 200)

# Test 9: Valid payment to same user
print("\n[TEST 9] Register user and send valid payment")
response = requests.post(f"{BASE_URL}/api/users/register", json={
    "name": "Charlie Brown",
    "email": "charlie@example.com",
    "upi_id": "charlie@axis",
    "phone": "9876543212",
    "initial_balance": 5000
})
print_response("Register Charlie", response, 200)

# Send valid payment from Charlie to Alice
response = requests.post(f"{BASE_URL}/api/payments/send", json={
    "sender_upi": "charlie@axis",
    "receiver_upi": "alice@axis",
    "amount": 250,
    "description": "Valid payment",
    "pin": "1234"
})
print_response("Valid Payment Charlie to Alice", response, 200)

# Test 10: Check transaction count
print("\n[TEST 10] Verify transaction count for Alice")
response = requests.get(f"{BASE_URL}/api/payments/transactions/alice@axis")
print_response("Alice's Transaction History", response, 200)

print("\n" + "="*60)
print("ADVANCED TEST CASES COMPLETED!")
print("="*60)
