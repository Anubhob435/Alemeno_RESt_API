# Credit Approval System

A Django REST API system for credit approval based on historical loan data and customer profiles.

## Features

- Customer registration with automatic credit limit calculation
- Loan eligibility checking based on credit score
- Loan creation with compound interest calculations
- Loan and customer management APIs
- Background data ingestion from Excel files
- Credit scoring algorithm based on payment history

## Setup Instructions

### Prerequisites

- Python 3.8+
- pip
- Redis (for Celery background tasks)

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd Alemeno_RESt_API
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run database migrations:
```bash
python manage.py migrate
```

4. Ingest initial data from Excel files:
```bash
python manage.py ingest_data
```

5. Create a superuser (optional):
```bash
python manage.py createsuperuser
```

6. Start the development server:
```bash
python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/api/`

### Background Tasks (Optional)

To run background tasks with Celery:

1. Start Redis server:
```bash
redis-server
```

2. Start Celery worker:
```bash
celery -A Alemeno_RESt_API worker --loglevel=info
```

## API Endpoints

### 1. Register Customer
- **URL:** `POST /api/register/`
- **Description:** Register a new customer
- **Request Body:**
```json
{
    "first_name": "John",
    "last_name": "Doe",
    "age": 30,
    "monthly_income": 50000,
    "phone_number": 9876543210
}
```

### 2. Check Loan Eligibility
- **URL:** `POST /api/check-eligibility/`
- **Description:** Check if a customer is eligible for a loan
- **Request Body:**
```json
{
    "customer_id": 1,
    "loan_amount": 500000,
    "interest_rate": 10.5,
    "tenure": 24
}
```

### 3. Create Loan
- **URL:** `POST /api/create-loan/`
- **Description:** Create a new loan for an eligible customer
- **Request Body:**
```json
{
    "customer_id": 1,
    "loan_amount": 500000,
    "interest_rate": 10.5,
    "tenure": 24
}
```

### 4. View Loan Details
- **URL:** `GET /api/view-loan/<loan_id>/`
- **Description:** Get details of a specific loan

### 5. View Customer Loans
- **URL:** `GET /api/view-loans/<customer_id>/`
- **Description:** Get all current loans for a customer

## Credit Scoring Algorithm

The system calculates credit scores based on:

1. **Past loans paid on time (40% weight)**
2. **Number of loans taken (20% weight)**
3. **Loan activity in current year (20% weight)**
4. **Loan approved volume vs limit (20% weight)**

### Approval Logic

- **Credit Score > 50:** Approve loan
- **30 < Credit Score ≤ 50:** Approve with interest rate ≥ 12%
- **10 < Credit Score ≤ 30:** Approve with interest rate ≥ 16%
- **Credit Score ≤ 10:** Reject loan

Additional constraints:
- Sum of current EMIs must not exceed 50% of monthly salary
- Sum of current loans must not exceed approved limit

## Testing

Run the test script to verify API functionality:

```bash
python test_apis.py
```

## Database Schema

### Customer Model
- `customer_id` (Primary Key)
- `first_name`
- `last_name`
- `age`
- `phone_number`
- `monthly_salary`
- `approved_limit` (calculated as 36 × monthly_salary, rounded to nearest lakh)
- `current_debt`

### Loan Model
- `loan_id` (Primary Key)
- `customer` (Foreign Key)
- `loan_amount`
- `tenure` (in months)
- `interest_rate`
- `monthly_repayment` (calculated using compound interest)
- `emis_paid_on_time`
- `start_date`
- `end_date`

## Docker Setup (Future)

The application is designed to be dockerized with PostgreSQL. Docker configuration will be added in future updates.

## Technologies Used

- Django 5.1.7
- Django REST Framework
- PostgreSQL (configured, currently using SQLite)
- Celery + Redis (for background tasks)
- Pandas (for Excel data processing)
- OpenPyXL (for Excel file reading)