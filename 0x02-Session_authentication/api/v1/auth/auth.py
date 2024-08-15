#!/usr/bin/env python3
"""Auth class"""
from typing import List, TypeVar
import re
from flask import request


class Auth:
    """Authentication class module
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Require authentication
        Args:
            path (str): path to check
            excluded_paths (List[str]): excluded paths
        Returns:
            bool: return True if path is not in the list of excluded paths
        """
        if not path or not excluded_paths:
            return True

        # Ensure path ends with a slash for consistent comparison
        path = path.rstrip('/') + '/'

        for excluded_path in excluded_paths:
            excluded_path = excluded_path.rstrip('/') + '/'
            if excluded_path.endswith('*'):
                if path.startswith(excluded_path[:-1]):
                    return False
            elif path == excluded_path:
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """Authorization header
        Args:
            request (_type_, optional):Defaults to None.
        Returns:
            str: Authorization header
        """
        if request:
            return request.headers.get('Authorization')
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Current user
        Returns:
            _type_: new user
        """
        return None
