#!/bin/bash

API_URL="https://alemeno-rest-api.onrender.com/api"

echo "🚀 Testing Deployed Credit Approval API"
echo "========================================"

echo ""
echo "1. 🏥 Health Check:"
curl -s "$API_URL/" | python -m json.tool

echo ""
echo "2. 👤 Register New Customer:"
curl -s -X POST "$API_URL/register/" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "John",
    "last_name": "Doe",
    "age": 30,
    "monthly_income": 60000,
    "phone_number": 9876543210
  }' | python -m json.tool

echo ""
echo "3. 💰 Check Loan Eligibility (Customer ID: 1):"
curl -s -X POST "$API_URL/check-eligibility/" \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": 1,
    "loan_amount": 500000,
    "interest_rate": 12.0,
    "tenure": 24
  }' | python -m json.tool

echo ""
echo "4. 🏦 Create Loan (Customer ID: 1):"
curl -s -X POST "$API_URL/create-loan/" \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": 1,
    "loan_amount": 300000,
    "interest_rate": 11.5,
    "tenure": 18
  }' | python -m json.tool

echo ""
echo "5. 📊 View Customer Loans (Customer ID: 1):"
curl -s "$API_URL/view-loans/1/" | python -m json.tool

echo ""
echo "✅ API Testing Complete!"
echo "🌐 Your API is live at: $API_URL"