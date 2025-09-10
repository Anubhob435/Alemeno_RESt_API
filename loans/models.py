from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal
import math


class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    age = models.IntegerField(validators=[MinValueValidator(18), MaxValueValidator(100)])
    phone_number = models.BigIntegerField()
    monthly_salary = models.DecimalField(max_digits=12, decimal_places=2)
    approved_limit = models.DecimalField(max_digits=12, decimal_places=2)
    current_debt = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    def save(self, *args, **kwargs):
        if not self.approved_limit:
            # approved_limit = 36 * monthly_salary (rounded to nearest lakh)
            limit = self.monthly_salary * 36
            # Round to nearest lakh (100,000)
            self.approved_limit = round(limit / 100000) * 100000
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    class Meta:
        db_table = 'customers'


class Loan(models.Model):
    loan_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='loans')
    loan_amount = models.DecimalField(max_digits=12, decimal_places=2)
    tenure = models.IntegerField()  # in months
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    monthly_repayment = models.DecimalField(max_digits=12, decimal_places=2)
    emis_paid_on_time = models.IntegerField(default=0)
    start_date = models.DateField()
    end_date = models.DateField()
    
    def calculate_monthly_installment(self):
        """Calculate monthly installment using compound interest formula"""
        principal = float(self.loan_amount)
        rate = float(self.interest_rate) / 100 / 12  # monthly rate
        n = self.tenure
        
        if rate == 0:
            return principal / n
        
        # EMI = P * r * (1 + r)^n / ((1 + r)^n - 1)
        emi = principal * rate * (1 + rate) ** n / ((1 + rate) ** n - 1)
        return round(emi, 2)
    
    def save(self, *args, **kwargs):
        if not self.monthly_repayment:
            self.monthly_repayment = self.calculate_monthly_installment()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Loan {self.loan_id} - {self.customer}"
    
    class Meta:
        db_table = 'loans'