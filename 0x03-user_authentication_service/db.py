#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.session import Session

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
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
        '''
            add_user: instance method
            @email: String representing the email.
            @hashed_password: String representing the hashed password.
            return: the User Object created.
        '''
        try:
            user = User(email=email, hashed_password=hashed_password)
            self._session.add(user)
            self._session.commit()
        except Exception:
            self._session.rollback()
            user = None
        return user

    def find_user_by(self, **kwargs) -> User:
        '''
            find_user_by: instance method.
            @kwargs: list of keyworded arguments.
            return: the User Object.
        '''
        for key, value in kwargs.items():
            if not hasattr(User, key):
                raise InvalidRequestError()
        res = self._session.query(User).filter_by(**kwargs).first()
        if res is None:
            raise NoResultFound()
        return res

    def update_user(self, user_id, **kwargs) -> None:
        '''
            update_user: instance method.
            @user_id: User ID.
            @kwargs: list of keyworded arguments.
            return: None
        '''
        user = self.find_user_by(id=user_id)
        if user:
            for key, value in kwargs.items():
                if hasattr(User, key):
                    setattr(user, key, value)
                else:
                    raise ValueError()
            self._session.commit()
