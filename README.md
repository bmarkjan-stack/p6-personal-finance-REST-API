# Personal Finance REST API

A RESTful backend API built with Python and Flask for managing personal income and expenses.

This project demonstrates backend development, REST API architecture, authentication, database integration, input validation, error handling, and automated testing.


## Project Structure

```text
personal-finance-api/
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── extensions.py
│   ├── models.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   └── transactions.py
│   └── utils/
│       ├── __init__.py
│       └── validation.py
├── tests/
│   ├── __init__.py
│   └── test_transactions.py
├── .env.example
├── .gitignore
├── README.md
├── requirements.txt
└── run.py