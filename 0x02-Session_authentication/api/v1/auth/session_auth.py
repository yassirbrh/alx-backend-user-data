#!/usr/bin/env python3
'''
    Module to manage the Session authentication
'''
from .auth import Auth
import base64
import binascii
from models.user import User
import re
from typing import TypeVar


class SessionAuth(Auth):
    '''
        Class SessionAuth handles the Session authentication.
    '''
    pass
