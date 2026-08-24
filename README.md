# Personal Finance REST API

A RESTful backend API built with Python and Flask for managing personal income and expenses.

This project demonstrates backend development, REST API architecture, authentication, database integration, input validation, error handling, and automated testing.

## Features

- User registration
- User login
- JWT authentication
- Create transactions
- Read transactions
- Update transactions
- Delete transactions
- SQLite database
- SQLAlchemy ORM
- Input validation
- JSON responses
- HTTP status codes
- Error handling
- User-specific transactions
- Automated tests
- CORS support

## Technologies

- Python
- Flask
- Flask-SQLAlchemy
- SQLite
- Flask-JWT-Extended
- Flask-CORS
- pytest
- python-dotenv

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