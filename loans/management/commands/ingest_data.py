from django.core.management.base import BaseCommand
from loans.tasks import ingest_all_data
import pandas as pd
from loans.models import Customer, Loan
from datetime import datetime
import os
from django.conf import settings


class Command(BaseCommand):
    help = 'Ingest customer and loan data from Excel files'

    def handle(self, *args, **options):
        # Check if data already exists to avoid duplicate ingestion
        if Customer.objects.exists():
            self.stdout.write(
                self.style.WARNING('Data already exists. Skipping ingestion.')
            )
            return
            
        self.stdout.write('Starting data ingestion...')
        
        # Ingest customer data
        self.stdout.write('Ingesting customer data...')
        customer_result = self.ingest_customer_data()
        self.stdout.write(customer_result)
        
        # Ingest loan data
        self.stdout.write('Ingesting loan data...')
        loan_result = self.ingest_loan_data()
        self.stdout.write(loan_result)
        
        self.stdout.write(
            self.style.SUCCESS('Data ingestion completed successfully!')
        )

    def ingest_customer_data(self):
        """Ingest customer data from Excel file"""
        try:
            customer_file = os.path.join(settings.BASE_DIR, 'customer_data.xlsx')
            df = pd.read_excel(customer_file)
            
            created_count = 0
            updated_count = 0
            
            for _, row in df.iterrows():
                customer, created = Customer.objects.get_or_create(
                    customer_id=row['Customer ID'],
                    defaults={
                        'first_name': row['First Name'],
                        'last_name': row['Last Name'],
                        'phone_number': row['Phone Number'],
                        'monthly_salary': row['Monthly Salary'],
                        'approved_limit': row['Approved Limit'],
                        'current_debt': 0,  # Not in the data
                        'age': row['Age']
                    }
                )
                
                if created:
                    created_count += 1
                else:
                    updated_count += 1
            
            return f"Customer data: Created {created_count}, Updated {updated_count}"
        
        except Exception as e:
            return f"Error ingesting customer data: {str(e)}"

    def ingest_loan_data(self):
        """Ingest loan data from Excel file"""
        try:
            loan_file = os.path.join(settings.BASE_DIR, 'loan_data.xlsx')
            df = pd.read_excel(loan_file)
            
            created_count = 0
            updated_count = 0
            
            for _, row in df.iterrows():
                try:
                    customer = Customer.objects.get(customer_id=row['Customer ID'])
                    
                    # Parse dates
                    start_date = pd.to_datetime(row['Date of Approval']).date()
                    end_date = pd.to_datetime(row['End Date']).date()
                    
                    loan, created = Loan.objects.get_or_create(
                        loan_id=row['Loan ID'],
                        defaults={
                            'customer': customer,
                            'loan_amount': row['Loan Amount'],
                            'tenure': row['Tenure'],
                            'interest_rate': row['Interest Rate'],
                            'monthly_repayment': row['Monthly payment'],
                            'emis_paid_on_time': row['EMIs paid on Time'],
                            'start_date': start_date,
                            'end_date': end_date
                        }
                    )
                    
                    if created:
                        created_count += 1
                    else:
                        updated_count += 1
                        
                except Customer.DoesNotExist:
                    self.stdout.write(f"Customer {row['Customer ID']} not found for loan {row['Loan ID']}")
                    continue
            
            return f"Loan data: Created {created_count}, Updated {updated_count}"
        
        except Exception as e:
            return f"Error ingesting loan data: {str(e)}"