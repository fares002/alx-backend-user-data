#!/usr/bin/env python3
"""Flask view that handles all routes for the Session authentication"""
from flask import jsonify, abort, request, make_response
from api.v1.views import app_views
from models.user import User
import os


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def auth_session():
    """Handle user login"""
    email = request.form.get('email')
    password = request.form.get('password')

    if not email:
        return jsonify({"error": "email missing"}), 400
    if not password:
        return jsonify({"error": "password missing"}), 400

    users = User.search({"email": email})
    if not users:
        return jsonify({"error": "no user found for this email"}), 404

    user = users[0]
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    from api.v1.app import auth  # Import to avoid circular imports
    session_id = auth.create_session(user.id)

    response = make_response(user.to_json())
    SESSION_NAME = os.getenv('SESSION_NAME', '_my_session_id')
    response.set_cookie(SESSION_NAME, session_id)

    return response


@app_views.route('/auth_session/logout', methods=['DELETE'],
                 strict_slashes=False)
def handle_logout():
    """
    Handle user logout
    """
    from api.v1.app import auth
    if auth.destroy_session(request):
        return jsonify({}), 200
    abort(404)
