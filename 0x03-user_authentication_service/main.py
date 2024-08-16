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
resettoken = auth.get_reset_password_token(email="faresosama002@gmail.com")