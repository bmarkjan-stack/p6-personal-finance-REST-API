from datetime import date as date_type
from datetime import datetime

ALLOWED_TRANSACTION_TYPES = {
    "income",
    "expense"
}


def validate_transaction(data):
    errors = {}

    if not isinstance(data, dict):
        return {
            "body": "Request body must be a JSON object."
        }

    description = data.get("description")
    amount = data.get("amount")
    category = data.get("category")
    transaction_type = data.get("type")
    transaction_date = data.get("date")

    if not description:
        errors["description"] = "Description is required."
    elif not isinstance(description, str):
        errors["description"] = "Description must be a string."
    elif len(description.strip()) < 2:
        errors["description"] = (
            "Description must contain at least 2 characters."
        )

    if amount is None:
        errors["amount"] = "Amount is required."
    else:
        try:
            amount = float(amount)

            if amount <= 0:
                errors["amount"] = "Amount must be greater than 0."

        except (TypeError, ValueError):
            errors["amount"] = "Amount must be a valid number."

    if not category:
        errors["category"] = "Category is required."
    elif not isinstance(category, str):
        errors["category"] = "Category must be a string."

    if not transaction_type:
        errors["type"] = "Transaction type is required."
    elif transaction_type not in ALLOWED_TRANSACTION_TYPES:
        errors["type"] = (
            "Type must be either 'income' or 'expense'."
        )

    if not transaction_date:
        errors["date"] = "Date is required."
    else:
        try:
            datetime.strptime(
                transaction_date,
                "%Y-%m-%d"
            )
        except ValueError:
            errors["date"] = (
                "Date must use YYYY-MM-DD format."
            )

    return errors