from flask import Blueprint, jsonify, request
from ..extensions import db
from ..models import User
from flask_jwt_extended import create_access_token

auth_bp = Blueprint("auth", __name__)

@auth_bp.post("/register")
def register():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            "error": "Request body must contain JSON."
        }), 400

    username = data.get("username", "").strip()
    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    errors = {}

    if not username:
        errors["username"] = "Username is required."
    elif len(username) < 3:
        errors["username"] = (
            "Username must be at least 3 characters."
        )

    if not email:
        errors["email"] = "Email is required."
    elif "@" not in email:
        errors["email"] = "Please provide a valid email."

    if not password:
        errors["password"] = "Password is required."
    elif len(password) < 6:
        errors["password"] = (
            "Password must be at least 6 characters."
        )

    if errors:
        return jsonify({
            "error": "Validation failed.",
            "details": errors
        }), 400

    if User.query.filter_by(username=username).first():
        return jsonify({
            "error": "Username is already registered."
        }), 409

    if User.query.filter_by(email=email).first():
        return jsonify({
            "error": "Email is already registered."
        }), 409

    user = User(
        username=username,
        email=email
    )

    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    return jsonify({
        "message": "User registered successfully.",
        "user": user.to_dict()
    }), 201

@auth_bp.post("/login")
def login():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            "error": "Request body must contain JSON."
        }), 400

    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    user = User.query.filter_by(email=email).first()

    if not user or not user.check_password(password):
        return jsonify({
            "error": "Invalid email or password."
        }), 401

    access_token = create_access_token(
        identity=str(user.id)
    )

    return jsonify({
        "message": "Login successful.",
        "access_token": access_token,
        "user": user.to_dict()
    }), 200