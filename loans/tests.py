from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from decimal import Decimal
from .models import Customer, Loan
from datetime import date, timedelta


class CustomerModelTest(TestCase):
    def test_customer_creation(self):
        """Test customer creation with automatic approved limit calculation"""
        customer = Customer.objects.create(
            first_name="John",
            last_name="Doe",
            age=30,
            phone_number=9876543210,
            monthly_salary=50000
        )
        
        # approved_limit should be 36 * 50000 = 1800000 (rounded to nearest lakh)
        expected_limit = 1800000
        self.assertEqual(customer.approved_limit, expected_limit)
        self.assertEqual(str(customer), "John Doe")


class LoanModelTest(TestCase):
    def setUp(self):
        self.customer = Customer.objects.create(
            first_name="Jane",
            last_name="Smith",
            age=25,
            phone_number=9876543211,
            monthly_salary=60000
        )

    def test_loan_creation(self):
        """Test loan creation with automatic EMI calculation"""
        loan = Loan.objects.create(
            customer=self.customer,
            loan_amount=500000,
            tenure=24,
            interest_rate=12.0,
            start_date=date.today(),
            end_date=date.today() + timedelta(days=730)
        )
        
        # EMI should be calculated automatically
        self.assertGreater(loan.monthly_repayment, 0)
        self.assertEqual(str(loan), f"Loan {loan.loan_id} - Jane Smith")


class APITestCase(APITestCase):
    def setUp(self):
        self.customer = Customer.objects.create(
            first_name="Test",
            last_name="Customer",
            age=35,
            phone_number=9876543212,
            monthly_salary=75000,
            approved_limit=2700000
        )

    def test_register_customer(self):
        """Test customer registration API"""
        url = reverse('register_customer')
        data = {
            'first_name': 'New',
            'last_name': 'Customer',
            'age': 28,
            'monthly_income': 55000,
            'phone_number': 9876543213
        }
        
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('customer_id', response.data)
        self.assertEqual(response.data['name'], 'New Customer')

    def test_check_eligibility(self):
        """Test loan eligibility check API"""
        url = reverse('check_eligibility')
        data = {
            'customer_id': self.customer.customer_id,
            'loan_amount': 500000,
            'interest_rate': 10.5,
            'tenure': 24
        }
        
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('approval', response.data)
        self.assertIn('monthly_installment', response.data)

    def test_create_loan(self):
        """Test loan creation API"""
        url = reverse('create_loan')
        data = {
            'customer_id': self.customer.customer_id,
            'loan_amount': 500000,
            'interest_rate': 10.5,
            'tenure': 24
        }
        
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('loan_approved', response.data)

    def test_view_loans(self):
        """Test view customer loans API"""
        # Create a loan first
        loan = Loan.objects.create(
            customer=self.customer,
            loan_amount=300000,
            tenure=12,
            interest_rate=11.0,
            start_date=date.today(),
            end_date=date.today() + timedelta(days=365)
        )
        
        url = reverse('view_loans', kwargs={'customer_id': self.customer.customer_id})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        if response.data:
            self.assertIn('loan_id', response.data[0])

    def test_invalid_customer(self):
        """Test API with invalid customer ID"""
        url = reverse('check_eligibility')
        data = {
            'customer_id': 99999,
            'loan_amount': 500000,
            'interest_rate': 10.5,
            'tenure': 24
        }
        
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)