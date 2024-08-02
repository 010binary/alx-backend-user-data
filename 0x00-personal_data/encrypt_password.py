#!/usr/bin/env python3
"""
encrypting and validating passwords using the bcrypt library.
Functions:
- hash_password(password: str)
    -> bytes: Hashes a password using bcrypt.
- is_valid(hashed_password: bytes, password: str)
    -> bool: Validates a password against a hashed password using bcrypt.
"""

import bcrypt


def hash_password(password: str) -> bytes:
    """Implement a hash_password function that takes a string

    Args:
        password (str): password

    Returns:
        bytes: hashed password
    """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """_summary_

    Args:
        hashed_password (bytes): 
        password (str): 
    Returns:
        bool: 
    """
    return bcrypt.checkpw(password.encode(), hashed_password)