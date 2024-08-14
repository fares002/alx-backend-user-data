#!/usr/bin/env python3
"""Authentication module.
"""
from typing import List, TypeVar


class Auth:
    """Authintacation """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Checks if authentication is required for a
        given path based on a list of excluded paths.

        Parameters:
        - path (str): The path to check.
        - excluded_paths (List[str]):
        A list of paths that do not require authentication.
        Paths can include a wildcard '*' at the end.

        Returns:
        - bool: True if the path is None,
        if excluded_paths is None or empty, or if the path is not
        in excluded_paths. Returns False if the path matches any
        of the excluded paths or
        the pattern specified by the wildcard '*'.
        """
        if path is None:
            return True
        if excluded_paths is None or len(excluded_paths) == 0:
            return True

        # Normalize the input path by stripping trailing slashes
        normalized_path = path.rstrip('/')

        for excluded_path in excluded_paths:
            # Normalize the excluded_path and handle wildcard '*'
            normalized_excluded_path = excluded_path.rstrip('/')

            if normalized_excluded_path.endswith('*'):
                # Remove the wildcard character and normalize the prefix
                prefix = normalized_excluded_path[:-1]
                # Check if the normalized path starts with the prefix
                if (normalized_path.startswith(prefix) and
                        len(normalized_path) >= len(prefix)):
                    return False
            else:
                # Normal case: exact match
                if normalized_path == normalized_excluded_path:
                    return False

        return True

    def authorization_header(self, request=None) -> str:
        """ Method to get authorization header.
        """
        if request is not None:
            return request.headers.get('Authorization', None)
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ Method to get user from request.
        """
        return None
