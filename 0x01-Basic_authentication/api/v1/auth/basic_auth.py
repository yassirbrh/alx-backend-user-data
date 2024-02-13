#!/usr/bin/env python3
'''
    Module to manage the Basic authentication
'''
from .auth import Auth
import re


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
        return re.search(r'Basic (.*)', authorization_header)
