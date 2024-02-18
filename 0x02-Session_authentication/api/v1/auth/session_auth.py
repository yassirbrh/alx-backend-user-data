#!/usr/bin/env python3
'''
    Module to manage the Session authentication
'''
from .auth import Auth
import uuid
from models.user import User


class SessionAuth(Auth):
    '''
        Class SessionAuth handles the Session authentication.
    '''
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        '''
            create_session: instance method.
            @self: Class instance.
            @user_id: User ID.
            return: The Session ID.
        '''
        if user_id is None or type(user_id) != str:
            return None
        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        '''
            user_id_for_session_id: instance method.
            @self: Class instance.
            @session_id: Session ID.
            return: The User ID based on the Session ID.
        '''
        if session_id is None or not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        '''
            current_user: Instance method.
            @self: Class Instance.
            @request: Flask request object.
            return: The current user.
        '''
        if request is None:
            return None
        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)
        return User.get(user_id)

    def destroy_session(self, request=None):
        '''
            destroy_session: instance method.
            @self: Class instance.
            @request: The flask request object.
            return: True if destroyed otherwise False.
        '''
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if session_id is None:
            return False
        user_id = self.user_id_for_session_id(session_id)
        if not user_id:
            return False
        try:
            del self.user_id_by_session_id[session_id]
        except Exception:
            pass
        return True