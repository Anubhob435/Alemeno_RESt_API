# Credit Approval System - Project Report

## Overview

This is a Django REST API system for a credit approval system that evaluates loan eligibility based on customer profiles and historical loan data. The system implements a complete workflow from customer registration to loan approval with background data processing capabilities.

## Project Structure

```
Alemeno_RESt_API/
├── Alemeno_RESt_API/           # Main Django project configuration
│   ├── __init__.py
│   ├── asgi.py
│   ├── celery.py               # Celery configuration for background tasks
│   ├── settings.py             # Django settings (SQLite by default, PostgreSQL commented)
│   ├── urls.py                 # Main URL routing
│   └── wsgi.py
├── loans/                      # Main application
│   ├── management/             # Custom management commands
│   │   └── commands/
│   │       └── ingest_data.py  # Data ingestion command
│   ├── migrations/             # Database migrations
│   ├── models.py               # Customer and Loan models
│   ├── serializers.py          # API serializers
│   ├── tasks.py                # Celery background tasks
│   ├── urls.py                 # Application URL routing
│   └── views.py                # API endpoints implementation
├── customer_data.xlsx          # Customer data for ingestion
├── loan_data.xlsx              # Loan data for ingestion
├── docker-compose.yml          # Docker configuration with PostgreSQL and Redis
├── Dockerfile                  # Application Docker configuration
├── manage.py                   # Django management script
├── requirements.txt            # Python dependencies
├── test_apis.py                # API testing script
├── README.md                   # Project documentation
└── assignment_requirements.md  # Original assignment requirements
```

## Implemented Features

### 1. Data Models

#### Customer Model
- `customer_id`: Auto-incrementing primary key
- `first_name`: Customer's first name
- `last_name`: Customer's last name
- `age`: Customer's age (18-100)
- `phone_number`: Customer's phone number
- `monthly_salary`: Customer's monthly income
- `approved_limit`: Credit limit calculated as 36 × monthly_salary, rounded to nearest lakh
- `current_debt`: Current outstanding debt (default: 0)

#### Loan Model
- `loan_id`: Auto-incrementing primary key
- `customer`: Foreign key to Customer model
- `loan_amount`: Total loan amount
- `tenure`: Loan duration in months
- `interest_rate`: Annual interest rate
- `monthly_repayment`: Monthly EMI calculated using compound interest formula
- `emis_paid_on_time`: Number of EMIs paid on time
- `start_date`: Loan start date
- `end_date`: Loan end date

### 2. API Endpoints

#### POST `/api/register/`
Registers a new customer with automatic credit limit calculation.

**Request:**
```json
{
    "first_name": "string",
    "last_name": "string", 
    "age": "integer",
    "monthly_income": "decimal",
    "phone_number": "integer"
}
```

**Response:**
```json
{
    "customer_id": "integer",
    "name": "string",
    "age": "integer",
    "monthly_income": "decimal",
    "approved_limit": "decimal",
    "phone_number": "integer"
}
```

#### POST `/api/check-eligibility/`
Checks loan eligibility based on customer's credit score.

**Request:**
```json
{
    "customer_id": "integer",
    "loan_amount": "decimal",
    "interest_rate": "decimal",
    "tenure": "integer"
}
```

**Response:**
```json
{
    "customer_id": "integer",
    "approval": "boolean",
    "interest_rate": "decimal",
    "corrected_interest_rate": "decimal",
    "tenure": "integer",
    "monthly_installment": "decimal"
}
```

#### POST `/api/create-loan/`
Processes a new loan application based on eligibility.

**Request:**
```json
{
    "customer_id": "integer",
    "loan_amount": "decimal",
    "interest_rate": "decimal",
    "tenure": "integer"
}
```

**Response:**
```json
{
    "loan_id": "integer/null",
    "customer_id": "integer",
    "loan_approved": "boolean",
    "message": "string",
    "monthly_installment": "decimal"
}
```

#### GET `/api/view-loan/<loan_id>/`
Retrieves details of a specific loan.

**Response:**
```json
{
    "loan_id": "integer",
    "customer": {
        "id": "integer",
        "first_name": "string",
        "last_name": "string",
        "phone_number": "integer",
        "age": "integer"
    },
    "loan_amount": "decimal",
    "interest_rate": "decimal",
    "monthly_installment": "decimal",
    "tenure": "integer"
}
```

#### GET `/api/view-loans/<customer_id>/`
Retrieves all current loans for a specific customer.

**Response:**
```json
[
    {
        "loan_id": "integer",
        "loan_amount": "decimal",
        "interest_rate": "decimal",
        "monthly_installment": "decimal",
        "repayments_left": "integer"
    }
]
```

### 3. Credit Scoring Algorithm

The system calculates credit scores (0-100) based on:

1. **Past loans paid on time (40% weight)**
2. **Number of loans taken (20% weight)**
3. **Loan activity in current year (20% weight)**
4. **Loan approved volume vs limit (20% weight)**

#### Loan Approval Logic

- **Credit Score > 50:** Approve loan
- **30 < Credit Score ≤ 50:** Approve with interest rate ≥ 12%
- **10 < Credit Score ≤ 30:** Approve with interest rate ≥ 16%
- **Credit Score ≤ 10:** Reject loan

Additional constraints:
- Sum of current EMIs must not exceed 50% of monthly salary
- Sum of current loans must not exceed approved limit

### 4. Background Data Processing

The system uses Celery with Redis for background data ingestion from Excel files:

#### Customer Data Ingestion
Processes `customer_data.xlsx` with columns:
- Customer ID
- First Name
- Last Name
- Age
- Phone Number
- Monthly Salary
- Approved Limit

#### Loan Data Ingestion
Processes `loan_data.xlsx` with columns:
- Customer ID
- Loan ID
- Loan Amount
- Tenure
- Interest Rate
- Monthly payment
- EMIs paid on Time
- Date of Approval
- End Date

## Technology Stack

- **Framework**: Django 5.1.7 with Django REST Framework 3.15.2
- **Database**: SQLite (currently) with PostgreSQL support configured
- **Background Processing**: Celery 5.3.4 with Redis 5.0.1
- **Data Processing**: Pandas 2.2.2 with OpenPyXL 3.1.2
- **Containerization**: Docker with docker-compose

## Current Issues and Improvements Needed

### 1. Database Configuration
The application is currently configured to use SQLite but should use PostgreSQL as per requirements. The PostgreSQL configuration is commented out in settings.py.

### 2. Data Ingestion Tasks
The Celery tasks in `loans/tasks.py` need to be updated to match the actual column names in the Excel files, which differ from the model field names.

### 3. Docker Configuration
The Docker setup needs to be verified to ensure all services (PostgreSQL, Redis, web app, Celery worker) work together correctly.

### 4. Credit Scoring Algorithm
The credit scoring implementation should be reviewed for accuracy and alignment with the assignment requirements.

## Setup and Usage

### Prerequisites
- Python 3.8+
- Docker and docker-compose (recommended)
- Redis server (for development without Docker)

### Installation with Docker (Recommended)
1. Run `docker-compose up` to start all services
2. In another terminal, run migrations: `docker-compose exec web python manage.py migrate`
3. Ingest data: `docker-compose exec web python manage.py ingest_data`

### Manual Installation
1. Install dependencies: `pip install -r requirements.txt`
2. Start Redis server for Celery
3. Run database migrations: `python manage.py migrate`
4. Ingest data: `python manage.py ingest_data`
5. Start development server: `python manage.py runserver`
6. Start Celery worker (optional): `celery -A Alemeno_RESt_API worker --loglevel=info`

## Testing

The system includes a test script (`test_apis.py`) that verifies all API endpoints with sample data. Run it with: `python test_apis.py`

## Conclusion

The credit approval system is largely implemented with all required API endpoints and background processing capabilities. The main tasks remaining are:
1. Switching from SQLite to PostgreSQL
2. Correcting data ingestion tasks to match Excel file formats
3. Validating and refining the credit scoring algorithm
4. Ensuring the Docker configuration works correctly