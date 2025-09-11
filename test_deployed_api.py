import requests
import json
import time

# Your deployed API URL
BASE_URL = "https://alemeno-rest-api.onrender.com/api"

def test_api_health():
    """Test API health and database connection"""
    print("🏥 Testing API Health...")
    
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API Status: {data.get('status', 'unknown')}")
            print(f"✅ Database: {data.get('database', 'unknown')}")
            print(f"✅ Version: {data.get('version', 'unknown')}")
            return True
        else:
            print(f"❌ Health check failed with status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

def test_register_customer():
    """Test customer registration on deployed API"""
    print("\n👤 Testing Customer Registration...")
    
    data = {
        "first_name": "Alice",
        "last_name": "Johnson", 
        "age": 28,
        "monthly_income": 75000,
        "phone_number": 9876543999
    }
    
    try:
        response = requests.post(f"{BASE_URL}/register/", json=data)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 201:
            result = response.json()
            print(f"✅ Customer registered successfully!")
            print(f"   Customer ID: {result['customer_id']}")
            print(f"   Name: {result['name']}")
            print(f"   Approved Limit: ${result['approved_limit']:,}")
            return result['customer_id']
        else:
            print(f"❌ Registration failed: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Registration error: {e}")
        return None

def test_check_eligibility(customer_id):
    """Test loan eligibility check"""
    print(f"\n💰 Testing Loan Eligibility for Customer {customer_id}...")
    
    data = {
        "customer_id": customer_id,
        "loan_amount": 500000,
        "interest_rate": 12.5,
        "tenure": 36
    }
    
    try:
        response = requests.post(f"{BASE_URL}/check-eligibility/", json=data)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Eligibility check completed!")
            print(f"   Approval: {'✅ APPROVED' if result['approval'] else '❌ REJECTED'}")
            print(f"   Interest Rate: {result['interest_rate']}%")
            print(f"   Corrected Rate: {result['corrected_interest_rate']}%")
            print(f"   Monthly EMI: ${result['monthly_installment']:,.2f}")
            return result
        else:
            print(f"❌ Eligibility check failed: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Eligibility check error: {e}")
        return None

def test_create_loan(customer_id):
    """Test loan creation"""
    print(f"\n🏦 Testing Loan Creation for Customer {customer_id}...")
    
    data = {
        "customer_id": customer_id,
        "loan_amount": 300000,
        "interest_rate": 11.5,
        "tenure": 24
    }
    
    try:
        response = requests.post(f"{BASE_URL}/create-loan/", json=data)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Loan creation completed!")
            print(f"   Loan Approved: {'✅ YES' if result['loan_approved'] else '❌ NO'}")
            print(f"   Loan ID: {result.get('loan_id', 'N/A')}")
            print(f"   Message: {result['message']}")
            print(f"   Monthly EMI: ${result['monthly_installment']:,.2f}")
            return result.get('loan_id')
        else:
            print(f"❌ Loan creation failed: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Loan creation error: {e}")
        return None

def test_view_loan(loan_id):
    """Test viewing loan details"""
    if not loan_id:
        print("\n⚠️  Skipping loan view test (no loan ID)")
        return
        
    print(f"\n📋 Testing View Loan {loan_id}...")
    
    try:
        response = requests.get(f"{BASE_URL}/view-loan/{loan_id}/")
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Loan details retrieved!")
            print(f"   Loan ID: {result['loan_id']}")
            print(f"   Customer: {result['customer']['first_name']} {result['customer']['last_name']}")
            print(f"   Amount: ${result['loan_amount']:,}")
            print(f"   Interest Rate: {result['interest_rate']}%")
            print(f"   Tenure: {result['tenure']} months")
        else:
            print(f"❌ View loan failed: {response.text}")
    except Exception as e:
        print(f"❌ View loan error: {e}")

def test_view_customer_loans(customer_id):
    """Test viewing customer's loans"""
    print(f"\n📊 Testing View Customer {customer_id} Loans...")
    
    try:
        response = requests.get(f"{BASE_URL}/view-loans/{customer_id}/")
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Customer loans retrieved!")
            print(f"   Number of active loans: {len(result)}")
            
            for i, loan in enumerate(result, 1):
                print(f"   Loan {i}:")
                print(f"     - ID: {loan['loan_id']}")
                print(f"     - Amount: ${loan['loan_amount']:,}")
                print(f"     - EMI: ${loan['monthly_installment']:,.2f}")
                print(f"     - Repayments Left: {loan['repayments_left']}")
        else:
            print(f"❌ View customer loans failed: {response.text}")
    except Exception as e:
        print(f"❌ View customer loans error: {e}")

def test_existing_customer():
    """Test with an existing customer from the database"""
    print("\n🔍 Testing with Existing Customer (ID: 1)...")
    
    # Test eligibility
    eligibility = test_check_eligibility(1)
    
    # Test loan creation
    loan_id = test_create_loan(1)
    
    # Test view loan
    if loan_id:
        test_view_loan(loan_id)
    
    # Test view customer loans
    test_view_customer_loans(1)

def run_comprehensive_test():
    """Run all API tests"""
    print("🚀 Starting Comprehensive API Test for Deployed Application")
    print("=" * 60)
    
    # Test API health
    if not test_api_health():
        print("❌ API health check failed. Stopping tests.")
        return
    
    print("\n" + "=" * 60)
    print("🧪 Testing with NEW customer...")
    
    # Test with new customer
    customer_id = test_register_customer()
    
    if customer_id:
        # Test eligibility
        eligibility = test_check_eligibility(customer_id)
        
        # Test loan creation
        loan_id = test_create_loan(customer_id)
        
        # Test view loan
        if loan_id:
            test_view_loan(loan_id)
        
        # Test view customer loans
        test_view_customer_loans(customer_id)
    
    print("\n" + "=" * 60)
    print("🧪 Testing with EXISTING customer...")
    
    # Test with existing customer
    test_existing_customer()
    
    print("\n" + "=" * 60)
    print("✅ All API tests completed!")
    print(f"🌐 API is live at: {BASE_URL}")

if __name__ == "__main__":
    run_comprehensive_test()