#!/usr/bin/env python3
"""auth system
"""
from bcrypt import hashpw, gensalt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from bcrypt import checkpw
from uuid import uuid4
from typing import Union


def _hash_password(password: str) -> bytes:
    """Hash password function

    Args:
        password (str): password to hash

    Returns:
        bytes: hashed password
    """
    return hashpw(password.encode('utf-8'), gensalt())


def _generate_uuid() -> str:
    """Generate uuid4 as string

    Returns:
        str: uuid4 as string
    """
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Register user

        Args:
            email (str): email
            password (str): password

        Raises:
            ValueError: if user already exists

        Returns:
            User: new user
        """
        try:
            user = self._db.find_user_by(email=email)
            if user:
                raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hashed_password = _hash_password(password)
            new_user = self._db.add_user(email, hashed_password)
        return new_user

    def valid_login(self, email: str, password: str) -> bool:
        """Valid login

        Args:
            email (str): email
            password (str): password

        Returns:
            bool: True if valid, False otherwise
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False

        user_password = user.hashed_password
        encoded_password = password.encode()

        if checkpw(encoded_password, user_password):
            return True

        return False

    def create_session(self, email: str) -> Union[str, None]:
        """Create session

        Args:
            email (str): email

        Returns:
            Union[str, None]: session id or None
        """
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """get user from session id

        Args:
            session_id (str): session id

        Returns:
            Union[User, None]: user or None
        """
        try:
            return self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None

    def destroy_session(self, user_id: str) -> None:
        """destroy session

        Args:
            user_id (str): user id

        Returns:
            _type_: None
        """
        self._db.update_user(user_id, session_id=None)
        return None

    def get_reset_password_token(self, email: str) -> str:
        """get reset password token

        Args:
            email (str): email

        Raises:
            ValueError: user not found

        Returns:
            str: reset token
        """
        try:
            user = self._db.find_user_by(email=email)
        except (NoResultFound, InvalidRequestError):
            raise ValueError

        user.reset_token = _generate_uuid()
        return user.reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """_summary_

        Args:
            reset_token (str): reset token
            password (str): New password

        Raises:
            ValueError: user not found

        Returns:
            _type_: None
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except Exception:
            raise ValueError

        hashed_password = _hash_password(password)
        self._db.update_user(
            user.id,
            hashed_password=hashed_password,
            reset_token=None
        )
        return None
