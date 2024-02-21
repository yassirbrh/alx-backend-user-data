#!/usr/bin/env python3
'''
    Module for handling authentication system.
'''
import bcrypt
from db import DB
from sqlalchemy.orm.exc import NoResultFound
from user import User


def _hash_password(password: str) -> bytes:
    '''
        _hash_password: function
        @password: Password to encrypt.
        return: the hashed password.
    '''
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        '''
            register_user: instance method
            @email: Email.
            @password: Password.
            return: User Object.
        '''
        hashed = _hash_password(password)
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return self._db.add_user(email, hashed)
        raise ValueError("User {} already exists".format(email))
