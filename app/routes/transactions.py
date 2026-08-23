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

@transactions_bp.get("")
@jwt_required()
def get_transactions():
    user_id = int(get_jwt_identity())

    transactions = (
        Transaction.query
        .filter_by(user_id=user_id)
        .order_by(Transaction.created_at.desc())
        .all()
    )

    return jsonify({
        "count": len(transactions),
        "transactions": [
            transaction.to_dict()
            for transaction in transactions
        ]
    }), 200

@transactions_bp.get("/<int:transaction_id>")
@jwt_required()
def get_transaction(transaction_id):
    user_id = int(get_jwt_identity())

    transaction = (
        Transaction.query
        .filter_by(
            id=transaction_id,
            user_id=user_id
        )
        .first()
    )

    if not transaction:
        return jsonify({
            "error": "Transaction not found."
        }), 404

    return jsonify({
        "transaction": transaction.to_dict()
    }), 200

@transactions_bp.put("/<int:transaction_id>")
@jwt_required()
def update_transaction(transaction_id):
    user_id = int(get_jwt_identity())

    transaction = (
        Transaction.query
        .filter_by(
            id=transaction_id,
            user_id=user_id
        )
        .first()
    )

    if not transaction:
        return jsonify({
            "error": "Transaction not found."
        }), 404

    data = request.get_json(silent=True)
    errors = validate_transaction(data)

    if errors:
        return jsonify({
            "error": "Validation failed.",
            "details": errors
        }), 400

    transaction.description = data["description"].strip()
    transaction.amount = float(data["amount"])
    transaction.category = data["category"].strip()
    transaction.type = data["type"]

    db.session.commit()

    return jsonify({
        "message": "Transaction updated successfully.",
        "transaction": transaction.to_dict()
    }), 200