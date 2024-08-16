#!/usr/bin/env python3
"""
Authentication module
"""
import bcrypt
from db import DB
from user import User
from uuid import uuid4
from sqlalchemy.orm.exc import NoResultFound


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """ Registers new user
            Args:
                - email: user's email
                - password: user's password
            Return:
                - User instance created
        """
        db = self._db
        try:
            user = db.find_user_by(email=email)
        except NoResultFound:
            user = db.add_user(email, _hash_password(password))
            return user
        else:
            raise ValueError(f"User {email} already exists")

    def valid_login(self, email: str, password: str) -> bool:
        """Credentials validation"""
        db = self._db
        try:
            user = db.find_user_by(email=email)
        except NoResultFound:
            return False

        if bcrypt.checkpw(password.encode('utf-8'), user.hashed_password):
            return True
        else:
            return False

    def create_session(self, email: str) -> str:
        """Creat session for the user"""
        db = self._db
        try:
            user = db.find_user_by(email=email)
        except NoResultFound:
            return False
        session_id = _generate_uuid()
        db.update_user(user.id, session_id=session_id)
        return session_id

    def get_user_from_session_id(self, session_id: str) -> User:
        """Get user by session id"""
        if session_id is None:
            return None
        db = self._db
        try:
            user = db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None
        return user

    def destroy_session(self, user_id: int) -> None:
        """destroy the user session
        Args:
            user_id: current user_id
        return:
            None
        """
        db = self._db
        db.update_user(user_id, session_id=None)
    
    def get_reset_password_token(self, email: str) -> str:
        """ generate a UUID and update the user’s 
            reset_token database field

        Args:
            email (str): user email

        Returns:
            str: token
        """
        db = self._db
        try:
            user = db.find_user_by(email=email)
        except NoResultFound:
            return None
        reset_token = _generate_uuid()
        db.update_user(user.id, reset_token=reset_token)
        return reset_token


def _hash_password(password: str) -> bytes:
    """ Creates password hash
        Args:
            - password: user password
        Return:
            - hashed password
    """
    e_pwd = password.encode()
    return bcrypt.hashpw(e_pwd, bcrypt.gensalt())


def _generate_uuid() -> str:
    """ Generates unique ids
        Return:
            - UUID generated
    """
    return str(uuid4())
