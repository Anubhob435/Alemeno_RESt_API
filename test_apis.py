import requests
import json

BASE_URL = "https://alemeno-rest-api.onrender.com/api/"

def test_register_customer():
    """Test customer registration"""
    print("Testing customer registration...")
    
    data = {
        "first_name": "John",
        "last_name": "Doe", 
        "age": 30,
        "monthly_income": 50000,
        "phone_number": 9876543210
    }
    
    response = requests.post(f"{BASE_URL}/register/", json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    if response.status_code == 201:
        return response.json()['customer_id']
    return None

def test_check_eligibility(customer_id):
    """Test loan eligibility check"""
    print(f"\nTesting loan eligibility for customer {customer_id}...")
    
    data = {
        "customer_id": customer_id,
        "loan_amount": 500000,
        "interest_rate": 10.5,
        "tenure": 24
    }
    
    response = requests.post(f"{BASE_URL}/check-eligibility/", json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    return response.json() if response.status_code == 200 else None

def test_create_loan(customer_id):
    """Test loan creation"""
    print(f"\nTesting loan creation for customer {customer_id}...")
    
    data = {
        "customer_id": customer_id,
        "loan_amount": 500000,
        "interest_rate": 10.5,
        "tenure": 24
    }
    
    response = requests.post(f"{BASE_URL}/create-loan/", json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    if response.status_code == 200 and response.json().get('loan_approved'):
        return response.json()['loan_id']
    return None

def test_view_loan(loan_id):
    """Test viewing loan details"""
    print(f"\nTesting view loan {loan_id}...")
    
    response = requests.get(f"{BASE_URL}/view-loan/{loan_id}/")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")

def test_view_loans(customer_id):
    """Test viewing customer loans"""
    print(f"\nTesting view loans for customer {customer_id}...")
    
    response = requests.get(f"{BASE_URL}/view-loans/{customer_id}/")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")

def test_existing_customer():
    """Test with existing customer from database"""
    print("\nTesting with existing customer (ID: 1)...")
    
    # Test eligibility check
    eligibility = test_check_eligibility(1)
    
    # Test loan creation
    loan_id = test_create_loan(1)
    
    if loan_id:
        # Test view loan
        test_view_loan(loan_id)
    
    # Test view loans
    test_view_loans(1)

if __name__ == "__main__":
    print("Starting API tests...")
    
    # Test with new customer
    customer_id = test_register_customer()
    
    if customer_id:
        eligibility = test_check_eligibility(customer_id)
        loan_id = test_create_loan(customer_id)
        
        if loan_id:
            test_view_loan(loan_id)
        
        test_view_loans(customer_id)
    
    # Test with existing customer
    test_existing_customer()
    
    print("\nAPI tests completed!")