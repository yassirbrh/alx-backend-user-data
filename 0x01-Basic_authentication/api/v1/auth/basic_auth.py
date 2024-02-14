#!/usr/bin/env python3
'''
    Module to manage the Basic authentication
'''
from .auth import Auth
import base64
import binascii
from models.user import User
import re
from typing import TypeVar


class BasicAuth(Auth):
    '''
        Class BasicAuth handles the Basic authentication.
    '''
    def extract_base64_authorization_header(
            self,
            authorization_header: str) -> str:
        '''
            extract_base64_authorization_header: instance method.
            @self: class instance.
            @authorization_header: Authorization Header.
            return: Base64 header.
        '''
        if authorization_header is None or type(authorization_header) != str:
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return re.search(r'Basic (.*)', authorization_header).group(1)

    def decode_base64_authorization_header(
            self,
            base64_authorization_header: str) -> str:
        '''
            decode_base64_authorization_header: function
            @self: class instance.
            @base64_authorization_header: Base64 encoded Authorization Header.
            return: decoded Base64 header.
        '''
        if base64_authorization_header:
            if type(base64_authorization_header) == str:
                try:
                    result = base64.b64decode(base64_authorization_header)
                    return result.decode('utf-8')
                except binascii.Error:
                    return None

    def extract_user_credentials(
            self,
            decoded_base64_authorization_header: str) -> (str, str):
        '''
            extract_user_credentials: function
            @self: class instance
            @decoded_base64_authorization_header
            return: user credentials
        '''
        if decoded_base64_authorization_header:
            if type(decoded_base64_authorization_header) == str:
                if ':' in decoded_base64_authorization_header:
                    user_data = decoded_base64_authorization_header.split(':')
                    return (user_data[0], user_data[1])
        return (None, None)

    def user_object_from_credentials(
            self,
            user_email: str, user_pwd: str) -> TypeVar('User'):
        '''
            user_object_from_credentials: function
            @self: class instance.
            @user_email: user email.
            @user_pwd: user password.
            return: The User Instance that had user email equals to user_email
        '''
        if user_email is None or type(user_email) != str:
            return None
        if user_pwd is None or type(user_pwd) != str:
            return None
        user = User.search({'email': user_email})
        if not user or user.is_valid_password(user_pwd):
            return None
        return user
