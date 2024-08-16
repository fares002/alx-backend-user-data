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
    if not Auth.valid_login(email, password):
        abort(401)
    session_id = Auth.create_session(email)
    reponse = jsonify({"email": email, "message": "logged in"})
    reponse.set_cookie("session_id", session_id)
    return reponse


@app.route('session', methods=['DELETE'])
def logout():
    """Log out endpoint
        Return:
            - redirect to the home page
    """
    session_id = request.cookies.get("session_id")
    user = Auth.get_user_from_session_id(session_id)
    if not user:
        abort(403)
    Auth.destroy_session(user.id)
    return redirect(url_for("home"))
    

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
