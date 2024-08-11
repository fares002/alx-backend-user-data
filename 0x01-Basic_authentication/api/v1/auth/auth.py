#!/usr/bin/env python3
from flask import request
from typing import List, TypeVar
from models import user

User = TypeVar('User')


class Auth:
    """
    Auth class provides methods for handling authentication and authorization.
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Checks if a path requires authentication based on excluded paths.

        Parameters:
        - path (str): The path to check.
        - excluded_paths (List[str]): A list of paths that do not require authentication.

        Returns:
        - bool: True if the path requires authentication, False otherwise.
        """
        if not path:
            return True
        if excluded_paths is None or len(excluded_paths) == 0:
            return True

        normalize_path = path.rstrip('/')

        for excluded_path in excluded_paths:
            normalized_excluded_path = excluded_path.rstrip('/')

            if normalized_excluded_path.endswith("*"):
                if normalize_path.startswith(normalized_excluded_path[:-1]):
                    return False
            else:
                if normalize_path == normalized_excluded_path:
                    return False

        return True

    def authorization_header(self, request=None) -> str:
        """
        Retrieves the Authorization header from the request.

        Parameters:
        - request: The Flask request object.

        Returns:
        - str: The value of the Authorization header if present, None otherwise.
        """
        if request is None:
            return None

        auth_header = request.headers.get('Authorization')
        return auth_header

    def current_user(self, request=None) -> User:
        """
        Retrieves the current user based on the request.

        Parameters:
        - request: The Flask request object.

        Returns:
        - User: The current user object if available, None otherwise.
        """
        if request is None:
            return None

