#!/usr/bin/env python3
"""Session Auth"""

from .auth import Auth
from models.user import User
import uuid

class SessionAuth(Auth):
    """Session Auth"""
    user_id_by_session_id = {}
    
    def create_session(self, user_id: str = None) -> str:
        """assing session id to user_id"""
        if user_id is None or not isinstance(user_id, str):
            return None
        
        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        
        return session_id
    
    def user_id_for_session_id(self, session_id: str = None) -> str:
        """return the user id based on the session id"""
        if session_id is None or not isinstance(session_id, str):
            return None
        
        return self.user_id_by_session_id.get(session_id)
    
    def current_user(self, request=None):
        """Return the User instance based on a session cookie"""
        if request is None:
            return None
        
        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)
        if user_id is None:
            return None
        
        return User.get(user_id)
    
    def destroy_session(self, request=None):
        """
        Deletes a user session
        """
        if request is None:
            return False
        session_cookie = self.session_cookie(request)
        if session_cookie is None:
            return False
        user_id = self.user_id_for_session_id(session_cookie)
        if user_id is None:
            return False
        del self.user_id_by_session_id[session_cookie]
        return True