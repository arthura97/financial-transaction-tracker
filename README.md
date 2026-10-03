# Financial Transaction Tracker

A banking-style **PostgreSQL + Python** application for managing users, bank accounts, balances, and financial transactions.

It demonstrates professional separation of concerns using:

* PostgreSQL for persistent data storage
* Python for application logic
* Repository pattern for database access
* Service layer for business logic
* Python models for domain entities
* PostgreSQL transactions for atomic financial operations
* Row-level locking for concurrent money operations
* Interactive command-line interface (CLI)

---

## 1. Project Overview

The Financial Transaction Tracker simulates core banking operations.

Users can:

* Create users
* Create bank accounts
* View users
* View accounts
* Check account balances
* Deposit money
* Withdraw money
* Transfer money between accounts
* View complete transaction history
* View recent transactions

The application maintains both:

1. The **current account balance**
2. A complete **transaction history**

Financial operations are executed atomically so that account balances and transaction records remain consistent.

---

## 2. Key Features

### User Management

* Create a new user
* Retrieve a user by ID
* Retrieve a user by email
* Prevent duplicate email addresses

### Account Management

* Create accounts for users
* Retrieve accounts by ID
* Retrieve accounts by account number
* Retrieve accounts belonging to a user
* Maintain current account balance
* Prevent negative account balances

### Financial Operations

#### Deposit

Adds money to an account and creates a:

```text
DEPOSIT
```

transaction.

#### Withdrawal

Removes money from an account and creates a:

```text
WITHDRAWAL
```

transaction.

Withdrawals are rejected when the account does not have sufficient funds.

#### Transfer

Transfers money between two accounts.

A transfer creates two transaction records:

```text
TRANSFER_OUT
TRANSFER_IN
```

The source account is debited and the destination account is credited as part of the same database transaction.

### Transaction History

Users can retrieve:

* Complete transaction history
* Recent transactions
* Transaction type
* Transaction amount
* Transaction timestamp

---

## 3. Architecture

The project follows a layered architecture:

```text
┌─────────────────────────────┐
│        Interactive CLI      │
│          main.py            │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│       Service Layer         │
│                             │
│  UserService                │
│  AccountService             │
│  TransactionService         │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│      Repository Layer       │
│                             │
│  UserRepository             │
│  AccountRepository          │
│  TransactionRepository      │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│         PostgreSQL          │
│                             │
│  users                      │
│  accounts                   │
│  transactions               │
└─────────────────────────────┘
```

### Layer Responsibilities

#### CLI Layer

Responsible for:

* Displaying the menu
* Reading user input
* Calling application services
* Displaying results and errors

The CLI does **not** contain SQL or banking business logic.

#### Service Layer

Responsible for:

* Business rules
* Validation
* Financial operations
* Transaction management
* Commit/rollback handling
* Coordinating multiple repositories

#### Repository Layer

Responsible for:

* SQL queries
* Database CRUD operations
* Mapping database rows to Python models
* PostgreSQL row locking

#### Model Layer

Represents domain entities:

```text
User
Account
Transaction
```

#### Database Layer

Responsible for:

* PostgreSQL connections
* Environment-based configuration
* Persistent storage

---

## 4. Database Design

The database contains three primary entities:

```text
User 1 ─────── N Account
                  │
                  │
                  ▼
              Transaction
                  N
```

### Users

Stores user information.

```text
users
├── id
├── name
├── email
└── created_at
```

### Accounts

Stores bank account information.

```text
accounts
├── id
├── user_id
├── account_number
├── balance
└── created_at
```

Each account belongs to exactly one user.

A user can have multiple accounts.

### Transactions

Stores all financial operations.

```text
transactions
├── id
├── account_id
├── transaction_type
├── amount
└── created_at
```

Supported transaction types:

```text
DEPOSIT
WITHDRAWAL
TRANSFER_IN
TRANSFER_OUT
```

---

## 5. Transfer Design

Transfers are represented using two transaction records.

For example:

```text
Account A ── $300 ──> Account B
```

creates:

```text
Account A
    └── TRANSFER_OUT  $300

Account B
    └── TRANSFER_IN   $300
```

The operation is executed atomically:

```text
BEGIN

Lock source account
Lock destination account

Update source balance
Update destination balance

Create TRANSFER_OUT
Create TRANSFER_IN

COMMIT
```

If any operation fails:

```text
ROLLBACK
```

This prevents situations where only part of a transfer is applied.

---

## 6. Concurrency and Row Locking

Financial operations use PostgreSQL row-level locking:

```sql
SELECT ...
FROM accounts
WHERE id = %s
FOR UPDATE;
```

This prevents concurrent operations from modifying the same account balance incorrectly.

For transfers, accounts are locked in deterministic account-ID order:

```text
lower account ID
       ↓
higher account ID
```

This reduces the risk of deadlocks when multiple transfers occur concurrently.

---

## 7. Money Handling

Financial amounts are handled using Python's:

```python
Decimal
```

rather than floating-point numbers.

PostgreSQL stores balances and transaction amounts using:

```sql
NUMERIC(15,2)
```

This avoids the precision problems associated with binary floating-point arithmetic.

Example:

```python
from decimal import Decimal

amount = Decimal("125.50")
```

---

## 8. Project Structure

```text
financial_transaction_tracker/
│
├── app/
│   ├── __init__.py
│   │
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py
│   │
│   ├── database/
│   │   ├── __init__.py
│   │   └── connection.py
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── account.py
│   │   └── transaction.py
│   │
│   ├── repositories/
│   │   ├── __init__.py
│   │   ├── user_repository.py
│   │   ├── account_repository.py
│   │   └── transaction_repository.py
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── user_service.py
│   │   ├── account_service.py
│   │   └── transaction_service.py
│   │
│   └── main.py
│
├── sql/
│   ├── schema.sql
│   └── seed.sql
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 9. Technologies

| Technology    | Purpose                        |
| ------------- | ------------------------------ |
| Python        | Application and business logic |
| PostgreSQL    | Relational database            |
| psycopg       | PostgreSQL database driver     |
| python-dotenv | Environment configuration      |
| SQL           | Database schema and queries    |

---

## 10. Requirements

Before running the project, install:

* Python 3.10+
* PostgreSQL
* pip

Verify Python:

```bash
python --version
```

Verify PostgreSQL:

```bash
psql --version
```

---

## 11. Installation

### 1. Clone the repository

```bash
git clone <repository-url>
```

Navigate into the project:

```bash
cd financial_transaction_tracker
```

### 2. Create a virtual environment

Windows:

```bash
python -m venv .venv
```

Activate it:

```bash
.venv\Scripts\activate
```

Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 12. PostgreSQL Setup

Create the database:

```sql
CREATE DATABASE financial_tracker;
```

Connect to it:

```bash
psql -U postgres -d financial_tracker
```

Run the schema:

```bash
psql -U postgres -d financial_tracker -f sql/schema.sql
```

Optional sample data:

```bash
psql -U postgres -d financial_tracker -f sql/seed.sql
```

---

## 13. Environment Configuration

Create a `.env` file in the project root:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=financial_tracker
DB_USER=postgres
DB_PASSWORD=your_postgresql_password
```

### Important

Do not commit `.env` to Git.

Add it to `.gitignore`:

```gitignore
.env
.venv/
__pycache__/
*.pyc
.pytest_cache/
```

---

## 14. Running the Application

From the project root:

```bash
python -m app.main
```

The application will display:

```text
============================================================
FINANCIAL TRANSACTION TRACKER
============================================================
1. Create User
2. View User
3. Create Account
4. View Account
5. Calculate Balance
6. Deposit
7. Withdraw
8. Transfer
9. View Transaction History
10. View Recent Transactions
0. Exit

Select an option:
```

---

## 15. Example Workflow

### Step 1 — Create a user

```text
Select an option: 1

============================================================
CREATE USER
============================================================

Enter name: Alice Smith
Enter email: alice@example.com

User created successfully.
```

### Step 2 — Create an account

```text
Select an option: 3

============================================================
CREATE ACCOUNT
============================================================

Enter user ID: 1
Enter account number: 100010
Enter initial balance: 1000

Account created successfully.
```

### Step 3 — Deposit money

```text
Select an option: 6

============================================================
DEPOSIT
============================================================

Enter account ID: 1
Enter deposit amount: 500

Deposit successful.
```

Balance becomes:

```text
1500.00
```

### Step 4 — Withdraw money

```text
Select an option: 7

Enter account ID: 1
Enter withdrawal amount: 200

Withdrawal successful.
```

Balance becomes:

```text
1300.00
```

### Step 5 — Transfer money

```text
Select an option: 8

Enter source account ID: 1
Enter destination account ID: 2
Enter transfer amount: 300

Transfer successful.
```

The resulting transaction history contains:

```text
TRANSFER_OUT   300.00
TRANSFER_IN    300.00
```

---

## 16. Database Transaction Management

The application follows the principle:

> A financial operation must either complete completely or have no effect.

For example, a transfer consists of:

```text
Update source balance
        +
Update destination balance
        +
Create outgoing transaction
        +
Create incoming transaction
```

All four operations belong to one PostgreSQL transaction.

```text
BEGIN
   │
   ├── Update source
   ├── Update destination
   ├── Insert TRANSFER_OUT
   └── Insert TRANSFER_IN
   │
   ▼
 COMMIT
```

If an exception occurs:

```text
ROLLBACK
```

This provides atomicity and protects financial consistency.

---

## 17. Validation Rules

The application validates important business rules.

### Users

* Name cannot be empty
* Email cannot be empty
* Email must be unique

### Accounts

* User must exist
* Account number must be unique
* Initial balance cannot be negative

### Deposits

* Amount must be greater than zero
* Account must exist

### Withdrawals

* Amount must be greater than zero
* Account must exist
* Sufficient funds are required

### Transfers

* Amount must be greater than zero
* Source account must exist
* Destination account must exist
* Source and destination must be different
* Source account must have sufficient funds

---

## 18. Design Principles Demonstrated

This project demonstrates several backend engineering concepts.

### Separation of Concerns

Each layer has a specific responsibility.

```text
CLI
 ↓
Services
 ↓
Repositories
 ↓
Database
```

### Repository Pattern

Database access is isolated inside repository classes.

### Service Layer

Business rules are separated from SQL queries.

### Dependency Injection

Services receive repositories through their constructors:

### Database Transactions

Financial operations use atomic PostgreSQL transactions.

### Row-Level Locking

`SELECT FOR UPDATE` protects account balances during concurrent operations.

### Data Integrity

PostgreSQL constraints enforce important database-level rules:

```text
PRIMARY KEY
FOREIGN KEY
UNIQUE
CHECK
NOT NULL
```

### Decimal Arithmetic

Financial values use decimal arithmetic instead of floating-point calculations.

---

## 19. Future Improvements

Possible extensions include:

### Authentication

Add:

* Password hashing
* Login
* User authentication
* Session management

### Account Features

Add:

* Account status
* Account types
* Currency
* Account closing
* Multiple currencies

### Transaction Features

Add:

* Transaction descriptions
* Transaction references
* Transfer IDs
* Transaction filtering
* Date-range queries
* Pagination

### Database Improvements

Add:

* Database indexes
* Connection pooling
* More advanced constraints
* Database migrations

### API Layer

The current CLI can later be replaced or supplemented with:

```text
FastAPI
    ↓
Services
    ↓
Repositories
    ↓
PostgreSQL
```

The existing service and repository architecture makes this transition easier because the business logic does not need to be placed inside API endpoints.

### Observability

Add:

* Structured logging
* Error logging
* Performance monitoring
* Database query monitoring

## 20. Learning Objectives

By completing this project, you practice:

* Python application structure
* PostgreSQL database design
* SQL
* Relational data modeling
* Foreign keys
* Constraints
* CRUD operations
* Python/PostgreSQL integration
* Repository pattern
* Service-layer architecture
* Dependency injection
* Database transactions
* Commit and rollback
* Row-level locking
* Concurrency considerations
* Decimal financial calculations
* CLI application development

---

## 24. License

This project is intended for educational and portfolio purposes.
