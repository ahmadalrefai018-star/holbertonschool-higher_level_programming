#!/usr/bin/python3
"""Protect API routes with Basic authentication and JWT."""

import os
import secrets

from flask import Flask, jsonify, request
from flask_httpauth import HTTPBasicAuth
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    get_jwt,
    jwt_required,
)
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = (
    os.environ.get("JWT_SECRET_KEY") or secrets.token_hex(32)
)

auth = HTTPBasicAuth()
jwt = JWTManager(app)

users = {
    "user1": {
        "username": "user1",
        "password": generate_password_hash("password"),
        "role": "user"
    },
    "admin1": {
        "username": "admin1",
        "password": generate_password_hash("password"),
        "role": "admin"
    }
}


@auth.verify_password
def verify_password(username, password):
    """Verify Basic authentication credentials."""
    user = users.get(username)
    if user and check_password_hash(user["password"], password):
        return username
    return None


@auth.error_handler
def basic_auth_error(status):
    """Return an authentication error."""
    return jsonify({"error": "Unauthorized"}), 401


@jwt.unauthorized_loader
def missing_token(reason):
    """Handle missing tokens."""
    return jsonify({"error": "Missing or invalid token"}), 401


@jwt.invalid_token_loader
def invalid_token(reason):
    """Handle invalid or malformed tokens."""
    return jsonify({"error": "Invalid token"}), 401


@jwt.expired_token_loader
def expired_token(jwt_header, jwt_payload):
    """Handle expired tokens."""
    return jsonify({"error": "Token has expired"}), 401


@jwt.revoked_token_loader
def revoked_token(jwt_header, jwt_payload):
    """Handle revoked tokens."""
    return jsonify({"error": "Token has been revoked"}), 401


@jwt.needs_fresh_token_loader
def fresh_token_required(jwt_header, jwt_payload):
    """Handle tokens that are not fresh."""
    return jsonify({"error": "Fresh token required"}), 401


@jwt.token_verification_failed_loader
def verification_failed(jwt_header, jwt_payload):
    """Handle failed token verification."""
    return jsonify({"error": "Token verification failed"}), 401


@app.route("/basic-protected")
@auth.login_required
def basic_protected():
    """Allow users with valid Basic credentials."""
    return "Basic Auth: Access Granted"


@app.route("/login", methods=["POST"])
def login():
    """Return an access token for valid credentials."""
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"error": "Invalid credentials"}), 401

    username = data.get("username")
    password = data.get("password")

    if not isinstance(username, str) or not isinstance(password, str):
        return jsonify({"error": "Invalid credentials"}), 401

    user = users.get(username)
    if not user or not check_password_hash(user["password"], password):
        return jsonify({"error": "Invalid credentials"}), 401

    token = create_access_token(
        identity=username,
        additional_claims={"role": user["role"]}
    )
    return jsonify({"access_token": token})


@app.route("/jwt-protected")
@jwt_required()
def jwt_protected():
    """Allow users with valid JWT tokens."""
    return "JWT Auth: Access Granted"


@app.route("/admin-only")
@jwt_required()
def admin_only():
    """Allow only users with the admin role."""
    if get_jwt().get("role") != "admin":
        return jsonify({"error": "Admin access required"}), 403

    return "Admin Access: Granted"


if __name__ == "__main__":
    app.run()
