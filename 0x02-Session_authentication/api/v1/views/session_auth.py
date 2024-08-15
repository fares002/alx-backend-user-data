#!/usr/bin/env python3
"""Flask view that handles all routes for the Session authentication"""
from flask import jsonify, abort, request, make_response
from api.v1.views import session_auth
from models.user import User
import os


@session_auth.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login():
    """login method"""
    email = request.form.get('email')
    if email is None:
        return jsonify({"error": "email missing"}), 400
    password = request.form.get('password')
    if password == None:
        return jsonify({"error": "email missing"}), 400
    
    if email:
        user = User.search({"email": email})
        if user is None:
            return jsonify({ "error": "no user found for this email" }), 404
        if user[0].is_valid_password(password) == False:
            return jsonify({ "error": "wrong password" }), 401
        from api.v1.app import auth
        session_id = auth.create_session(user[0].id)
        response = make_response(user.to_json())
        response.set_cookie(os.getenv('SESSION_NAME', '_my_session_id'), session_id)

        