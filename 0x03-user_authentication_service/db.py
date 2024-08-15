#!/usr/bin/env python3
"""
you will complete the DB class provided below to implement the add_user method
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from user import Base


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Adds a new user to the database and returns the User object
        """
        new_user = User(email=email, hashed_password=hashed_password)
        self._session.add(new_user)
        self._session.commit()
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """Finds a user by arbitrary keyword arguments
        Raises:
            NoResultFound: If no user is found
            InvalidRequestError: If invalid query arguments are passed
        """
        try:
            query = self._session.query(User).filter_by(**kwargs)
            user = query.one()
            return user
        except NoResultFound:
            raise NoResultFound("No user found with the provided filters.")
        except InvalidRequestError:
            raise InvalidRequestError("Invalid query arguments provided.")

    def update_user(self, user_id: int, **kwargs) -> None:
        """Updates a user's attributes and commits the changes to the database
        Raises:
            ValueError: If an argument does not correspond to a valid user attribute
        """
        user = self.find_user_by(id=user_id)
        for key, value in kwargs.items():
            if hasattr(user, key):
                setattr(user, key, value)
            else:
                raise ValueError(f"Invalid attribute: {key}")
        self._session.commit()
