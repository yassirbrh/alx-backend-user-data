#!/usr/bin/env python3
'''
    Module to manage the Session authentication
'''
from .auth import Auth
import uuid


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
        session_id = uuid.uuid4()
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        '''
            user_id_for_session_id: instance method.
            @self: Class instance.
            @session_id: Session ID.
            return: The User ID based on the Session ID.
        '''
        if session_id is None or type(session_id) != str:
            return None
        user_id = self.user_id_by_session_id.get(session_id)
        return user_id
