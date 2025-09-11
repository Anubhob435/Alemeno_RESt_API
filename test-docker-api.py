#!/usr/bin/env python
"""
Test Docker container API endpoints
"""
import requests
import time
import json

BASE_URL = "http://localhost:8000/api"

def wait_for_api():
    """Wait for API to be ready"""
    max_retries = 30
    for i in range(max_retries):
        try:
            response = requests.get(f"{BASE_URL}/", timeout=5)
            if response.status_code == 200:
                print("✅ API is ready!")
                return True
        except:
            pass
        print(f"⏳ Waiting for API... ({i+1}/{max_retries})")
        time.sleep(2)
    return False

def test_docker_api():
    """Test Docker container API"""
    print("🐳 Testing Docker Container API")
    print("=" * 40)
    
    if not wait_for_api():
        print("❌ API not ready after 60 seconds")
        return False
    
    # Test health check
    print("\n1. 🏥 Health Check:")
    try:
        response = requests.get(f"{BASE_URL}/")
        data = response.json()
        print(f"   Status: {data.get('status')}")
        print(f"   Database: {data.get('database')}")
        print(f"   Version: {data.get('version')}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    
    # Test eligibility check with existing customer
    print("\n2. 💰 Eligibility Check (Customer 1):")
    try:
        payload = {
            "customer_id": 1,
            "loan_amount": 300000,
            "interest_rate": 12.0,
            "tenure": 24
        }
        response = requests.post(f"{BASE_URL}/check-eligibility/", json=payload)
        data = response.json()
        print(f"   Approval: {'✅' if data.get('approval') else '❌'}")
        print(f"   Interest Rate: {data.get('interest_rate')}%")
        print(f"   Monthly EMI: ${float(data.get('monthly_installment', 0)):,.2f}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    
    # Test view customer loans
    print("\n3. 📊 View Customer Loans (Customer 1):")
    try:
        response = requests.get(f"{BASE_URL}/view-loans/1/")
        data = response.json()
        print(f"   Active Loans: {len(data)}")
        if data:
            loan = data[0]
            print(f"   Sample Loan ID: {loan.get('loan_id')}")
            print(f"   Amount: ${float(loan.get('loan_amount', 0)):,.2f}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    
    print("\n✅ Docker API test completed successfully!")
    print("🎯 Your Docker container is working perfectly!")
    return True

if __name__ == "__main__":
    test_docker_api()