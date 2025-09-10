from celery import shared_task
import pandas as pd
from datetime import datetime
from .models import Customer, Loan
import os
from django.conf import settings


@shared_task
def ingest_customer_data():
    """Background task to ingest customer data from Excel file"""
    try:
        # Read customer data
        customer_file = os.path.join(settings.BASE_DIR, 'customer_data.xlsx')
        df = pd.read_excel(customer_file)
        
        created_count = 0
        updated_count = 0
        
        for _, row in df.iterrows():
            customer, created = Customer.objects.get_or_create(
                customer_id=row['customer_id'],
                defaults={
                    'first_name': row['first_name'],
                    'last_name': row['last_name'],
                    'phone_number': row['phone_number'],
                    'monthly_salary': row['monthly_salary'],
                    'approved_limit': row['approved_limit'],
                    'current_debt': row.get('current_debt', 0),
                    'age': 25  # Default age since not in customer data
                }
            )
            
            if created:
                created_count += 1
            else:
                # Update existing customer
                customer.first_name = row['first_name']
                customer.last_name = row['last_name']
                customer.phone_number = row['phone_number']
                customer.monthly_salary = row['monthly_salary']
                customer.approved_limit = row['approved_limit']
                customer.current_debt = row.get('current_debt', 0)
                customer.save()
                updated_count += 1
        
        return f"Customer data ingestion completed. Created: {created_count}, Updated: {updated_count}"
    
    except Exception as e:
        return f"Error ingesting customer data: {str(e)}"


@shared_task
def ingest_loan_data():
    """Background task to ingest loan data from Excel file"""
    try:
        # Read loan data
        loan_file = os.path.join(settings.BASE_DIR, 'loan_data.xlsx')
        df = pd.read_excel(loan_file)
        
        created_count = 0
        updated_count = 0
        
        for _, row in df.iterrows():
            try:
                customer = Customer.objects.get(customer_id=row['customer_id'])
                
                # Parse dates
                start_date = pd.to_datetime(row['start_date']).date()
                end_date = pd.to_datetime(row['end_date']).date()
                
                loan, created = Loan.objects.get_or_create(
                    loan_id=row['loan_id'],
                    defaults={
                        'customer': customer,
                        'loan_amount': row['loan_amount'],
                        'tenure': row['tenure'],
                        'interest_rate': row['interest_rate'],
                        'monthly_repayment': row['monthly_repayment (emi)'],
                        'emis_paid_on_time': row['EMIs_paid_on_time'],
                        'start_date': start_date,
                        'end_date': end_date
                    }
                )
                
                if created:
                    created_count += 1
                else:
                    # Update existing loan
                    loan.customer = customer
                    loan.loan_amount = row['loan_amount']
                    loan.tenure = row['tenure']
                    loan.interest_rate = row['interest_rate']
                    loan.monthly_repayment = row['monthly_repayment (emi)']
                    loan.emis_paid_on_time = row['EMIs_paid_on_time']
                    loan.start_date = start_date
                    loan.end_date = end_date
                    loan.save()
                    updated_count += 1
                    
            except Customer.DoesNotExist:
                print(f"Customer with ID {row['customer_id']} not found for loan {row['loan_id']}")
                continue
        
        return f"Loan data ingestion completed. Created: {created_count}, Updated: {updated_count}"
    
    except Exception as e:
        return f"Error ingesting loan data: {str(e)}"


@shared_task
def ingest_all_data():
    """Background task to ingest both customer and loan data"""
    customer_result = ingest_customer_data()
    loan_result = ingest_loan_data()
    
    return f"Data ingestion completed. {customer_result}. {loan_result}"