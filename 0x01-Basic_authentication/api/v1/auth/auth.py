#!/usr/bin/env python3
'''
    Module to manage the API authentication
'''
from flask import request
from typing import List, TypeVar


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
        if not path or not excluded_paths or len(excluded_paths) == 0:
            return True
        if path.rstrip('/') in excluded_paths or path in excluded_paths:
            return False
        else:
            return True

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
