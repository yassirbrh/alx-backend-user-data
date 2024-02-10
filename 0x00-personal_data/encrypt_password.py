#!/usr/bin/env python3
'''
    Functions hash_password and is_valid
'''
import bcrypt


def hash_password(password: str) -> bytes:
    '''
        hash_password: function
        @password: password to hash.
        return: The hashed version of password.
    '''
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    '''
        is_valid: function
        @hashed_password: the hashed version of the password as bytes.
        @password: The password to check.
        return: True if the password is valid
                False otherwise.
    '''
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password)
