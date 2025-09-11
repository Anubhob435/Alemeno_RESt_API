#!/usr/bin/env python
"""Verify database connection and data"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Alemeno_RESt_API.settings')
django.setup()

from loans.models import Customer, Loan

def verify_database():
    print("🔍 Verifying database connection and data...")
    
    # Check customers
    customer_count = Customer.objects.count()
    print(f"✅ Customers in database: {customer_count}")
    
    # Check loans
    loan_count = Loan.objects.count()
    print(f"✅ Loans in database: {loan_count}")
    
    # Show sample customer
    if customer_count > 0:
        sample_customer = Customer.objects.first()
        print(f"📋 Sample customer: {sample_customer.first_name} {sample_customer.last_name}")
        print(f"   - Monthly Salary: ${sample_customer.monthly_salary:,}")
        print(f"   - Approved Limit: ${sample_customer.approved_limit:,}")
        
        # Show customer's loans
        customer_loans = sample_customer.loans.count()
        print(f"   - Number of loans: {customer_loans}")
    
    # Check database backend
    from django.db import connection
    print(f"🗄️  Database backend: {connection.vendor}")
    print(f"🗄️  Database name: {connection.settings_dict['NAME']}")
    print(f"🗄️  Database host: {connection.settings_dict['HOST']}")
    
    print("\n✅ Database verification completed successfully!")

if __name__ == "__main__":
    verify_database()