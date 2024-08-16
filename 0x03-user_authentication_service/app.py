#!/usr/bin/env python3
"""Basic Flask app"""
from flask import Flask, jsonify, request, abort, Response, redirect, url_for
from auth import Auth


app = Flask(__name__)
AUTH = Auth()


@app.route('/')
def home():
    """return {"message": "Bienvenue"}"""
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=["POST"], strict_slashes=False)
def users():
    """register a user"""
    email = request.form.get("email")
    password = request.form.get("password")
    try:
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login() -> Response:
    """ Login endpoint
        Form fields:
            - email
            - password
        Return:
            - user email and login message JSON represented
            - 401 if credential are invalid
    """
    email = request.form.get("email")
    password = request.form.get("password")
    if not email or not password:
        abort(401)
    if not AUTH.valid_login(email=email, password=password):
        abort(401)
    session_id = AUTH.create_session(email)
    reponse = jsonify({"email": email, "message": "logged in"})
    reponse.set_cookie("session_id", session_id)
    return reponse


@app.route('/sessions', methods=['DELETE'])
def logout():
    """Log out endpoint
        Return:
            - redirect to the home page
    """
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if not user:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect(url_for("home"))


@app.route('/profile', methods=['GET'])
def profile() -> str:
    """ User profile endpoint
        Return:
            - user email JSON represented
            - 403 if session_id is not linked to any user
    """
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if not user:
        abort(403)
    return jsonify({"email": user.email}), 200


@app.route('/reset_password', methods=['POST'])
def rest_password():
    """rest password endpoint"""
    email = request.form.get("email")
    try:
        reset_token = AUTH.get_reset_password_token(email)
    except ValueError:
        abort(403)
    return jsonify({"email": email, "reset_token": reset_token})


@app.route("/reset_password", methods=["PUT"])
def update_password():
    """ Password update endpoint
        Form fields:
            - email
            - reset_token
            - new_password
        Return:
            - user email and password update message JSON represented
            - 403 if reset token is not provided or not linked to any user
    """
    email = request.form.get("email")
    new_password = request.form.get("new_password")
    reset_token = request.form.get("reset_token")

    try:
        AUTH.update_password(reset_token, new_password)
    except ValueError:
        abort(403)
    return jsonify({"email": email, "message": "Password updated"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
