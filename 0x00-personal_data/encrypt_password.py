#!/usr/bin/env python3
'''
    Function hash_password that expects one string argument name password and
    returns a salted, hashed password, which is a byte string.
'''
import bcrypt


def hash_password(password: str) -> str:
    '''
        hash_password: function
        @password: password to hash.
        return: The hashed version of password.
    '''
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
