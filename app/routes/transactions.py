from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from ..utils.validation import validate_transaction
from ..models import Transaction
from ..extensions import db

transactions_bp = Blueprint(
    "transactions",
    __name__
)

@transactions_bp.post("")
@jwt_required()
def create_transaction():
    user_id = int(get_jwt_identity())
    data = request.get_json(silent=True)
    errors = validate_transaction(data)

    if errors:
        return jsonify({
            "error": "Validation failed.",
            "details": errors
        }), 400

    transaction = Transaction(
        description=data["description"].strip(),
        amount=float(data["amount"]),
        category=data["category"].strip(),
        type=data["type"],
        user_id=user_id
    )

    db.session.add(transaction)
    db.session.commit()

    return jsonify({
        "message": "Transaction created successfully.",
        "transaction": transaction.to_dict()
    }), 201