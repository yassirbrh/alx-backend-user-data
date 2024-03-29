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
            return: True if the path not excluded.
                    False otherwise.
        '''
        if not path or not excluded_paths or len(excluded_paths) == 0:
            return True
        for excluded_path in excluded_paths:
            if excluded_path[-1] == "*":
                if len(excluded_path[:-1]) <= len(path):
                    if path[0:len(excluded_path[:-1])] == excluded_path[:-1]:
                        return False
            if path.rstrip('/') == excluded_path.rstrip('/'):
                return False
        return True

    def authorization_header(self, request=None) -> str:
        '''
            authorization_header: instance method.
            @self: class instance.
            @request: the Flask request object.
            return: The Flask request object.
        '''
        if request is None:
            return None
        return request.headers.get('Authorization', None)

    def current_user(self, request=None) -> TypeVar('User'):
        '''
            current_user: instance method.
            @self: Class instance.
            @request: The flask request object.
            return: the current user.
        '''
        return None
