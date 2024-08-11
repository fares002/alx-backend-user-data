#!/usr/bin/env python3

from flask import request
from typing import List, TypeVar, Tuple, Optional
from models.user import User
from .auth import Auth
import base64

UserType = TypeVar('UserType', bound=User)

class BasicAuth(Auth):
    def extract_base64_authorization_header(self, authorization_header: str) -> Optional[str]:
        """
        Extracts the base64 authorization header from a string.

        Parameters:
        - authorization_header (str): The 'Authorization' header value.

        Returns:
        - Optional[str]: Base64 encoded authorization string if valid, else None.
        """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(self, base64_authorization_header: str) -> Optional[str]:
        """
        Decodes the base64 authorization header.

        Parameters:
        - base64_authorization_header (str): Base64 encoded authorization string.

        Returns:
        - Optional[str]: Decoded string if successful, else None.
        """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            decoded_bytes = base64.b64decode(base64_authorization_header)
            return decoded_bytes.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(self, decoded_base64_authorization_header: str) -> Tuple[Optional[str], Optional[str]]:
        """
        Extracts user credentials (email and password) from the decoded authorization header.

        Parameters:
        - decoded_base64_authorization_header (str): Decoded authorization header string.

        Returns:
        - Tuple[Optional[str], Optional[str]]: Tuple containing email and password if successful, else (None, None).
        """
        if decoded_base64_authorization_header is None:
            return (None, None)
        if not isinstance(decoded_base64_authorization_header, str):
            return (None, None)
        if ":" in decoded_base64_authorization_header:
            splited_auth_header = decoded_base64_authorization_header.split(":")
            email = splited_auth_header[0]
            password = ":".join(splited_auth_header[1:])
            return (email, password)
        return (None, None)

    def user_object_from_credentials(self, user_email: str, user_pwd: str) -> Optional[UserType]:
        """
        Retrieves a User object based on email and password credentials.

        Parameters:
        - user_email (str): User's email.
        - user_pwd (str): User's password.

        Returns:
        - Optional[UserType]: User object if credentials are valid, else None.
        """
        if not isinstance(user_email, str) or not isinstance(user_pwd, str):
            return None
        users = User.search({'email': user_email})

        if not users:
            return None
        user = users[0]

        if not user.is_valid_password(user_pwd):
            return None

        return user

    def current_user(self, request=None) -> Optional[UserType]:
        """
        Retrieves the current user based on the request's authorization header.

        Parameters:
        - request: The Flask request object.

        Returns:
        - Optional[UserType]: User object if authentication is successful, else None.
        """
        user_auth_header = self.authorization_header(request)
        user_extracted_auth_header = self.extract_base64_authorization_header(user_auth_header)
        user_decoded_auth_header = self.decode_base64_authorization_header(user_extracted_auth_header)
        user_credentials = self.extract_user_credentials(user_decoded_auth_header)
        if user_credentials:
            user_email, user_pwd = user_credentials
            return self.user_object_from_credentials(user_email, user_pwd)
        return None

