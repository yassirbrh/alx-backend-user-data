#!/usr/bin/env python3
'''
    Module for handling authentication system.
'''
import bcrypt
from db import DB
from sqlalchemy.orm.exc import NoResultFound
from user import User
import uuid


def _hash_password(password: str) -> bytes:
    '''
        _hash_password: function
        @password: Password to encrypt.
        return: the hashed password.
    '''
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def _generate_uuid() -> str:
    '''
        _generate_uuid: Instance method.
        return: String representation of uuid.
    '''
    return str(uuid.uuid4())


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

    def valid_login(self, email: str, password: str) -> bool:
        '''
            valid_login: Instance method.
            @email: Email to check.
            @password: Password to check after the email is checked.
            return: True if the login is valid.
                    False otherwise.
        '''
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False
        if bcrypt.checkpw(password.encode('utf-8'), user.hashed_password):
            return True
        return False

    def create_session(self, email: str) -> str:
        '''
            create_session: Instance method.
            @self: Class instance.
            @email: Email to look for.
            return: Session ID.
        '''
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None
        session_id = _generate_uuid()
        self._db.update_user(user.id, session_id=session_id)
        return session_id
