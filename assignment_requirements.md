---
# Assignment for Internship - Backend: Credit Approval System

In this assignment, you will be working on creating a credit approval system based on past data as well as future transactions. The goal is to assess proficiency with the Python/Django stack, using background tasks, and handling operations on Databases.

---

## 1. Setup and Initialization

### a) Setup
- Use **Django 4+** with **Django Rest Framework**.
- There is no requirement to make a frontend for the application.
- You need to build appropriate data models for the application.
- The entire application and all its dependencies should be **dockerized**.
- The application should use a **PostgreSQL DB**.

### b) Initialization
You are provided with two data files:

1. **`customer_data.xlsx`**: A table of existing customers with the following attributes:
   - `customer_id`
   - `first_name`
   - `last_name`
   - `phone_number`
   - `monthly_salary`
   - `approved_limit`
   - `current_debt`

2. **`loan_data.xlsx`**: A table of past and existing loans by customers with the following attributes:
   - `customer_id`
   - `loan_id`
   - `loan_amount`
   - `tenure`
   - `interest_rate`
   - `monthly_repayment (emi)`
   - `EMIs_paid_on_time`
   - `start_date`
   - `end_date`

You must ingest this provided data into the initial system using **background workers**.
---

## 2. APIs

You need to build the following API endpoints with appropriate error handling and status codes. Use a **compound interest scheme** for the calculation of monthly interest.

### • `/register`

This endpoint adds a new customer to the customer table with an approved limit based on their salary using the following relation:
$approved\_limit = 36 \times monthly\_salary$ (rounded to the nearest lakh).

**a) Request Body**
| Field            | Value                              |
| ---------------- | ---------------------------------- |
| `first_name`     | First Name of customer (string)    |
| `last_name`      | Last Name of customer (string)     |
| `age`            | Age of customer (int)              |
| `monthly_income` | Monthly income of individual (int) |
| `phone_number`   | Phone number (int)                 |

**b) Response Body**
| Field            | Value                              |
| ---------------- | ---------------------------------- |
| `customer_id`    | ID of customer (int)               |
| `name`           | Name of customer (string)          |
| `age`            | Age of customer (int)              |
| `monthly_income` | Monthly income of individual (int) |
| `approved_limit` | Approved credit limit (int)        |
| `phone_number`   | Phone number (int)                 |

### • `/check-eligibility`

This endpoint checks loan eligibility based on a customer's credit score (out of 100), which is calculated using historical loan data.

**Credit Score Components:**

- Past loans paid on time
- Number of loans taken in the past
- Loan activity in the current year
- Loan approved volume
- **If the sum of a customer's current loans > approved limit, the credit score is 0.**

**Loan Approval Logic:**

- **Credit Rating > 50:** Approve loan.
- **50 > Credit Rating > 30:** Approve loans with an interest rate > 12%.
- **30 > Credit Rating > 10:** Approve loans with an interest rate > 16%.
- **10 > Credit Rating:** Do not approve any loans.
- **If the sum of all current EMIs > 50% of monthly salary, do not approve the loan.**
- If the provided interest rate does not match the required slab based on the credit score, correct it in the response (e.g., if credit score is 20 and interest rate is 8%, the response should include `corrected_interest_rate = 16%`).

**a) Request Body**
| Field           | Value                         |
| --------------- | ----------------------------- |
| `customer_id`   | ID of customer (int)          |
| `loan_amount`   | Requested loan amount (float) |
| `interest_rate` | Interest rate on loan (float) |
| `tenure`        | Tenure of loan (int)          |

**b) Response Body**
| Field                     | Value                                                                                                  |
| ------------------------- | ------------------------------------------------------------------------------------------------------ |
| `customer_id`             | ID of customer (int)                                                                                   |
| `approval`                | Can loan be approved (bool)                                                                            |
| `interest_rate`           | Interest rate on loan (float)                                                                          |
| `corrected_interest_rate` | Corrected interest rate based on credit rating; same as `interest_rate` if it matches the slab (float) |
| `tenure`                  | Tenure of loan (int)                                                                                   |
| `monthly_installment`     | Monthly installment to be paid as repayment (float)                                                    |

### • `/create-loan`

This endpoint processes a new loan based on the eligibility check.

**a) Request Body**
| Field           | Value                         |
| --------------- | ----------------------------- |
| `customer_id`   | ID of customer (int)          |
| `loan_amount`   | Requested loan amount (float) |
| `interest_rate` | Interest rate on loan (float) |
| `tenure`        | Tenure of loan (int)          |

**b) Response Body**
| Field                 | Value                                                    |
| --------------------- | -------------------------------------------------------- |
| `loan_id`             | ID of approved loan, null otherwise (int)                |
| `customer_id`         | ID of customer (int)                                     |
| `loan_approved`       | Is the loan approved (bool)                              |
| `message`             | Appropriate message if the loan is not approved (string) |
| `monthly_installment` | Monthly installment to be paid as repayment (float)      |

### • `/view-loan/<loan_id>`

This endpoint views the details of a specific loan and the associated customer.

**a) Response Body**
| Field                 | Value                                                                                  |
| --------------------- | -------------------------------------------------------------------------------------- |
| `loan_id`             | ID of the approved loan (int)                                                          |
| `customer`            | JSON object containing customer `id`, `first_name`, `last_name`, `phone_number`, `age` |
| `loan_amount`         | Loan amount (float)                                                                    |
| `interest_rate`       | Interest rate of the approved loan (float)                                             |
| `monthly_installment` | Monthly installment to be paid as repayment (float)                                    |
| `tenure`              | Tenure of the loan (int)                                                               |

### • `/view-loans/<customer_id>`

This endpoint views all current loans for a specific customer.

**a) Response Body**
A list of loan items, where each item has the following structure:

| Field                 | Value                                               |
| --------------------- | --------------------------------------------------- |
| `loan_id`             | ID of the approved loan (int)                       |
| `loan_amount`         | Loan amount (float)                                 |
| `interest_rate`       | Interest rate of the approved loan (float)          |
| `monthly_installment` | Monthly installment to be paid as repayment (float) |
| `repayments_left`     | Number of EMIs left (int)                           |

---

## 3. General Guidelines

- Ensure good code quality, organization, and segregation of responsibilities.
- Adding unit tests is not necessary but will be considered for bonus points.
- The assignment should be submitted within **36 hours**.
- The entire application and its dependencies (like the DB) must be **dockerized** and should run from a single `docker-compose` command.
- Please submit the **GitHub link** of the repository.
