#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from user import User
from sqlalchemy.exc import NoResultFound, InvalidRequestError

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
        """Create new user instance 
        and save it to the database"""
        session = self._session
        try:
            new_user = User(email=email, hashed_password = hashed_password)
            session.add(new_user)
            session.commit()
        except Exception:
            session.rollback()
            new_user = None
        return new_user
    
    def find_user_by(self, **kwargs) -> User:
        """ Find user by a given attribute
            Args:
                - Dictionary of attributes to use as search
                parameters
            Return:
                - User object
        """

        session = self._session
        try:
            user = session.query(User).filter_by(**kwargs).first()
            if user is None:
                raise NoResultFound
            return user
        except NoResultFound:
            raise
        except InvalidRequestError:
            raise