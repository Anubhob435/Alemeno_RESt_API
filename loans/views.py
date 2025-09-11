from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Sum, Q
from django.http import JsonResponse
from datetime import datetime, date
from decimal import Decimal
import math

from .models import Customer, Loan
from .serializers import (
    CustomerRegistrationSerializer, CustomerRegistrationResponseSerializer,
    LoanEligibilitySerializer, LoanEligibilityResponseSerializer,
    LoanCreateSerializer, LoanCreateResponseSerializer,
    LoanDetailSerializer, CustomerLoanSerializer
)


def api_home(request):
    """API documentation home"""
    return JsonResponse({
        "message": "Credit Approval System API",
        "version": "1.0",
        "endpoints": {
            "register": "POST /api/register/ - Register a new customer",
            "check_eligibility": "POST /api/check-eligibility/ - Check loan eligibility",
            "create_loan": "POST /api/create-loan/ - Create a new loan",
            "view_loan": "GET /api/view-loan/<loan_id>/ - View loan details",
            "view_loans": "GET /api/view-loans/<customer_id>/ - View customer loans"
        },
        "documentation": "See README.md for detailed API documentation"
    })


def calculate_credit_score(customer):
    """Calculate credit score based on historical loan data"""
    loans = Loan.objects.filter(customer=customer)
    
    if not loans.exists():
        return 50  # Default score for new customers
    
    # Check if current loans exceed approved limit
    current_loans_sum = loans.aggregate(
        total=Sum('loan_amount')
    )['total'] or 0
    
    if current_loans_sum > customer.approved_limit:
        return 0
    
    # Calculate score components
    total_loans = loans.count()
    loans_paid_on_time = sum(1 for loan in loans if loan.emis_paid_on_time >= loan.tenure * 0.9)
    
    # Current year activity
    current_year = datetime.now().year
    current_year_loans = loans.filter(start_date__year=current_year).count()
    
    # Calculate score (simplified algorithm)
    score = 0
    
    # Past loans paid on time (40% weight)
    if total_loans > 0:
        on_time_ratio = loans_paid_on_time / total_loans
        score += on_time_ratio * 40
    
    # Number of loans (20% weight) - fewer loans is better
    if total_loans <= 3:
        score += 20
    elif total_loans <= 6:
        score += 15
    else:
        score += 10
    
    # Current year activity (20% weight) - moderate activity is good
    if current_year_loans <= 2:
        score += 20
    elif current_year_loans <= 4:
        score += 15
    else:
        score += 10
    
    # Loan approved volume (20% weight)
    if current_loans_sum <= customer.approved_limit * Decimal('0.5'):
        score += 20
    elif current_loans_sum <= customer.approved_limit * Decimal('0.8'):
        score += 15
    else:
        score += 10
    
    return min(100, max(0, score))


def get_required_interest_rate(credit_score):
    """Get minimum required interest rate based on credit score"""
    if credit_score > 50:
        return 0  # Any rate is acceptable
    elif credit_score > 30:
        return 12
    elif credit_score > 10:
        return 16
    else:
        return None  # No loan approval


def calculate_monthly_installment(loan_amount, interest_rate, tenure):
    """Calculate monthly installment using compound interest"""
    principal = float(loan_amount)
    rate = float(interest_rate) / 100 / 12  # monthly rate
    n = tenure
    
    if rate == 0:
        return Decimal(str(principal / n))
    
    # EMI = P * r * (1 + r)^n / ((1 + r)^n - 1)
    emi = principal * rate * (1 + rate) ** n / ((1 + rate) ** n - 1)
    return Decimal(str(round(emi, 2)))


@api_view(['POST'])
def register_customer(request):
    """Register a new customer"""
    serializer = CustomerRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        customer = serializer.save()
        response_serializer = CustomerRegistrationResponseSerializer(customer)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def check_eligibility(request):
    """Check loan eligibility for a customer"""
    serializer = LoanEligibilitySerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    data = serializer.validated_data
    customer_id = data['customer_id']
    loan_amount = data['loan_amount']
    interest_rate = data['interest_rate']
    tenure = data['tenure']
    
    try:
        customer = Customer.objects.get(customer_id=customer_id)
    except Customer.DoesNotExist:
        return Response({'error': 'Customer not found'}, status=status.HTTP_404_NOT_FOUND)
    
    # Calculate credit score
    credit_score = calculate_credit_score(customer)
    
    # Check EMI constraint (sum of all current EMIs should not exceed 50% of monthly salary)
    current_emis = Loan.objects.filter(
        customer=customer,
        end_date__gte=date.today()
    ).aggregate(total_emi=Sum('monthly_repayment'))['total_emi'] or Decimal('0')
    
    monthly_installment = calculate_monthly_installment(loan_amount, interest_rate, tenure)
    total_emi = current_emis + monthly_installment
    
    max_allowed_emi = customer.monthly_salary * Decimal('0.5')
    
    # Determine approval and correct interest rate
    required_rate = get_required_interest_rate(credit_score)
    approval = False
    corrected_interest_rate = interest_rate
    
    if credit_score <= 10:
        approval = False
    elif total_emi > max_allowed_emi:
        approval = False
    else:
        if required_rate is None:
            approval = False
        elif required_rate == 0 or interest_rate >= required_rate:
            approval = True
        else:
            approval = True
            corrected_interest_rate = required_rate
            monthly_installment = calculate_monthly_installment(loan_amount, corrected_interest_rate, tenure)
    
    response_data = {
        'customer_id': customer_id,
        'approval': approval,
        'interest_rate': interest_rate,
        'corrected_interest_rate': corrected_interest_rate,
        'tenure': tenure,
        'monthly_installment': monthly_installment
    }
    
    response_serializer = LoanEligibilityResponseSerializer(response_data)
    return Response(response_serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def create_loan(request):
    """Create a new loan"""
    serializer = LoanCreateSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    data = serializer.validated_data
    customer_id = data['customer_id']
    loan_amount = data['loan_amount']
    interest_rate = data['interest_rate']
    tenure = data['tenure']
    
    try:
        customer = Customer.objects.get(customer_id=customer_id)
    except Customer.DoesNotExist:
        return Response({'error': 'Customer not found'}, status=status.HTTP_404_NOT_FOUND)
    
    # Check eligibility first
    credit_score = calculate_credit_score(customer)
    current_emis = Loan.objects.filter(
        customer=customer,
        end_date__gte=date.today()
    ).aggregate(total_emi=Sum('monthly_repayment'))['total_emi'] or Decimal('0')
    
    monthly_installment = calculate_monthly_installment(loan_amount, interest_rate, tenure)
    total_emi = current_emis + monthly_installment
    max_allowed_emi = customer.monthly_salary * Decimal('0.5')
    
    required_rate = get_required_interest_rate(credit_score)
    
    # Check approval conditions
    loan_approved = False
    message = ""
    loan_id = None
    
    if credit_score <= 10:
        message = "Loan not approved due to low credit score"
    elif total_emi > max_allowed_emi:
        message = "Loan not approved due to high EMI burden"
    elif required_rate is None:
        message = "Loan not approved due to credit score"
    elif required_rate > 0 and interest_rate < required_rate:
        message = f"Loan not approved. Minimum interest rate required: {required_rate}%"
    else:
        # Create the loan
        loan_approved = True
        message = "Loan approved successfully"
        
        # Use corrected interest rate if needed
        final_interest_rate = max(interest_rate, required_rate) if required_rate > 0 else interest_rate
        monthly_installment = calculate_monthly_installment(loan_amount, final_interest_rate, tenure)
        
        start_date = date.today()
        end_date = date(start_date.year + (start_date.month + tenure - 1) // 12,
                       (start_date.month + tenure - 1) % 12 + 1,
                       start_date.day)
        
        loan = Loan.objects.create(
            customer=customer,
            loan_amount=loan_amount,
            tenure=tenure,
            interest_rate=final_interest_rate,
            monthly_repayment=monthly_installment,
            start_date=start_date,
            end_date=end_date
        )
        loan_id = loan.loan_id
    
    response_data = {
        'loan_id': loan_id,
        'customer_id': customer_id,
        'loan_approved': loan_approved,
        'message': message,
        'monthly_installment': monthly_installment
    }
    
    response_serializer = LoanCreateResponseSerializer(response_data)
    return Response(response_serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def view_loan(request, loan_id):
    """View details of a specific loan"""
    loan = get_object_or_404(Loan, loan_id=loan_id)
    serializer = LoanDetailSerializer(loan)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def view_loans(request, customer_id):
    """View all current loans for a customer"""
    customer = get_object_or_404(Customer, customer_id=customer_id)
    loans = Loan.objects.filter(customer=customer, end_date__gte=date.today())
    serializer = CustomerLoanSerializer(loans, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)