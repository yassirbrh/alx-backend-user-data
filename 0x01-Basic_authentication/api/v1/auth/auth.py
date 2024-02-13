#!/usr/bin/env python3
'''
    Module to manage the API authentication
'''
from flask import request
from typing import TypeVar


class Auth:
    '''
        Class Auth that handle the authentication system.
    '''
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        '''
            require_auth: instance method.
            @self: class instance.
            @path: The path.
            @excluded_paths: the excluded paths.
            return: True or False.
        '''
        return False

    def authorization_header(self, request=None) -> str:
        '''
            authorization_header: instance method.
            @self: class instance.
            @request: the Flask request object.
            return: The Flask request object.
        '''
        return request

    def current_user(self, request=None) -> TypeVar('User'):
        '''
            current_user: instance method.
            @self: Class instance.
            @request: The flask request object.
            return: the current user.
        '''
        return request
