#!/usr/bin/env python3
"""
Main file
"""
from db import DB
from user import User

from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from auth import Auth

auth = Auth()

auth = Auth()
email = "test@example.com"
password = "test123"
if auth.valid_login(email=email, password=password):
    print("Login Successful")
else:
    print("Login Failed")