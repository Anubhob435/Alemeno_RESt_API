---
# Assignment for Internship - Backend: Credit Approval System

In this assignment, you will be working on creating a credit approval system based on past data as well as future transactions. [cite_start]The goal is to assess proficiency with the Python/Django stack, using background tasks, and handling operations on Databases. [cite: 4]
---

## 1. Setup and Initialization

### [cite_start]a) Setup [cite: 6]

- [cite_start]Use **Django 4+** with **Django Rest Framework**. [cite: 7]
- [cite_start]There is no requirement to make a frontend for the application. [cite: 8]
- [cite_start]You need to build appropriate data models for the application. [cite: 9, 10]
- [cite_start]The entire application and all its dependencies should be **dockerized**. [cite: 11]
- [cite_start]The application should use a **PostgreSQL DB**. [cite: 12]

### [cite_start]b) Initialization [cite: 13]

You are provided with two data files:

1.  [cite_start]**`customer_data.xlsx`**: A table of existing customers with the following attributes: [cite: 14, 15]

    - [cite_start]`customer_id` [cite: 16]
    - [cite_start]`first_name` [cite: 17]
    - [cite_start]`last_name` [cite: 18]
    - [cite_start]`phone_number` [cite: 19]
    - [cite_start]`monthly_salary` [cite: 20]
    - [cite_start]`approved_limit` [cite: 21]
    - [cite_start]`current_debt` [cite: 22]

2.  [cite_start]**`loan_data.xlsx`**: A table of past and existing loans by customers with the following attributes: [cite: 23, 24]
    - [cite_start]`customer_id` [cite: 26]
    - [cite_start]`loan_id` [cite: 27]
    - [cite_start]`loan_amount` [cite: 28]
    - [cite_start]`tenure` [cite: 29]
    - [cite_start]`interest_rate` [cite: 30]
    - [cite_start]`monthly_repayment (emi)` [cite: 31]
    - [cite_start]`EMIs_paid_on_time` [cite: 32]
    - [cite_start]`start_date` [cite: 33]
    - [cite_start]`end_date` [cite: 34]

[cite_start]You must ingest this provided data into the initial system using **background workers**. [cite: 35]

---

## 2. APIs

[cite_start]You need to build the following API endpoints with appropriate error handling and status codes. [cite: 37] [cite_start]Use a **compound interest scheme** for the calculation of monthly interest. [cite: 38]

### • `/register`

[cite_start]This endpoint adds a new customer to the customer table with an approved limit based on their salary using the following relation: [cite: 39]
[cite_start]$approved\_limit = 36 \times monthly\_salary$ (rounded to the nearest lakh). [cite: 41]

[cite_start]**a) Request Body** [cite: 42]

| Field            | Value                              |
| ---------------- | ---------------------------------- |
| `first_name`     | First Name of customer (string)    |
| `last_name`      | Last Name of customer (string)     |
| `age`            | Age of customer (int)              |
| `monthly_income` | Monthly income of individual (int) |
| `phone_number`   | Phone number (int)                 |

[cite_start][cite: 43]

[cite_start]**b) Response Body** [cite: 44]

| Field            | Value                              |
| ---------------- | ---------------------------------- |
| `customer_id`    | ID of customer (int)               |
| `name`           | Name of customer (string)          |
| `age`            | Age of customer (int)              |
| `monthly_income` | Monthly income of individual (int) |
| `approved_limit` | Approved credit limit (int)        |
| `phone_number`   | Phone number (int)                 |

[cite_start][cite: 46]

### • `/check-eligibility`

[cite_start]This endpoint checks loan eligibility based on a customer's credit score (out of 100), which is calculated using historical loan data. [cite: 48, 49]

[cite_start]**Credit Score Components:** [cite: 49]

- [cite_start]Past loans paid on time [cite: 50]
- [cite_start]Number of loans taken in the past [cite: 51]
- [cite_start]Loan activity in the current year [cite: 53]
- [cite_start]Loan approved volume [cite: 55]
- [cite_start]**If the sum of a customer's current loans > approved limit, the credit score is 0.** [cite: 57]

[cite_start]**Loan Approval Logic:** [cite: 58]

- [cite_start]**Credit Rating > 50:** Approve loan. [cite: 59]
- [cite_start]**50 > Credit Rating > 30:** Approve loans with an interest rate > 12%. [cite: 60, 61]
- [cite_start]**30 > Credit Rating > 10:** Approve loans with an interest rate > 16%. [cite: 62]
- [cite_start]**10 > Credit Rating:** Do not approve any loans. [cite: 63]
- [cite_start]**If the sum of all current EMIs > 50% of monthly salary, do not approve the loan.** [cite: 64]
- [cite_start]If the provided interest rate does not match the required slab based on the credit score, correct it in the response (e.g., if credit score is 20 and interest rate is 8%, the response should include `corrected_interest_rate = 16%`). [cite: 65, 67]

[cite_start]**a) Request Body** [cite: 68]

| Field           | Value                         |
| --------------- | ----------------------------- |
| `customer_id`   | ID of customer (int)          |
| `loan_amount`   | Requested loan amount (float) |
| `interest_rate` | Interest rate on loan (float) |
| `tenure`        | Tenure of loan (int)          |

[cite_start][cite: 69]

[cite_start]**b) Response Body** [cite: 70]

| Field                     | Value                                                                                                  |
| ------------------------- | ------------------------------------------------------------------------------------------------------ |
| `customer_id`             | ID of customer (int)                                                                                   |
| `approval`                | Can loan be approved (bool)                                                                            |
| `interest_rate`           | Interest rate on loan (float)                                                                          |
| `corrected_interest_rate` | Corrected interest rate based on credit rating; same as `interest_rate` if it matches the slab (float) |
| `tenure`                  | Tenure of loan (int)                                                                                   |
| `monthly_installment`     | Monthly installment to be paid as repayment (float)                                                    |

[cite_start][cite: 71]

### • `/create-loan`

[cite_start]This endpoint processes a new loan based on the eligibility check. [cite: 72, 73]

[cite_start]**a) Request Body** [cite: 74]

| Field           | Value                         |
| --------------- | ----------------------------- |
| `customer_id`   | ID of customer (int)          |
| `loan_amount`   | Requested loan amount (float) |
| `interest_rate` | Interest rate on loan (float) |
| `tenure`        | Tenure of loan (int)          |

[cite_start][cite: 75]

[cite_start]**b) Response Body** [cite: 77]

| Field                 | Value                                                    |
| --------------------- | -------------------------------------------------------- |
| `loan_id`             | ID of approved loan, null otherwise (int)                |
| `customer_id`         | ID of customer (int)                                     |
| `loan_approved`       | Is the loan approved (bool)                              |
| `message`             | Appropriate message if the loan is not approved (string) |
| `monthly_installment` | Monthly installment to be paid as repayment (float)      |

[cite_start][cite: 78]

### • `/view-loan/<loan_id>`

[cite_start]This endpoint views the details of a specific loan and the associated customer. [cite: 79, 80]

[cite_start]**a) Response Body** [cite: 81]

| Field                 | Value                                                                                  |
| --------------------- | -------------------------------------------------------------------------------------- |
| `loan_id`             | ID of the approved loan (int)                                                          |
| `customer`            | JSON object containing customer `id`, `first_name`, `last_name`, `phone_number`, `age` |
| `loan_amount`         | Loan amount (float)                                                                    |
| `interest_rate`       | Interest rate of the approved loan (float)                                             |
| `monthly_installment` | Monthly installment to be paid as repayment (float)                                    |
| `tenure`              | Tenure of the loan (int)                                                               |

[cite_start][cite: 82]

### • `/view-loans/<customer_id>`

[cite_start]This endpoint views all current loans for a specific customer. [cite: 83, 84]

[cite_start]**a) Response Body** [cite: 85]
A list of loan items, where each item has the following structure:

| Field                 | Value                                               |
| --------------------- | --------------------------------------------------- |
| `loan_id`             | ID of the approved loan (int)                       |
| `loan_amount`         | Loan amount (float)                                 |
| `interest_rate`       | Interest rate of the approved loan (float)          |
| `monthly_installment` | Monthly installment to be paid as repayment (float) |
| `repayments_left`     | Number of EMIs left (int)                           |

[cite_start][cite: 87]

---

## 3. General Guidelines

- [cite_start]Ensure good code quality, organization, and segregation of responsibilities. [cite: 89]
- [cite_start]Adding unit tests is not necessary but will be considered for bonus points. [cite: 90]
- [cite_start]The assignment should be submitted within **36 hours**. [cite: 91]
- [cite_start]The entire application and its dependencies (like the DB) must be **dockerized** and should run from a single `docker-compose` command. [cite: 92, 93]
- [cite_start]Please submit the **GitHub link** of the repository. [cite: 94]
