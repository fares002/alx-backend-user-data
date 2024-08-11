from flask import request
from typing import List, TypeVar,Tuple, Optional
from models.user import User
from .auth import Auth
import base64

user = TypeVar('User')

class BasicAuth(Auth):
    def extract_base64_authorization_header(self, authorization_header: str) -> str:
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header[6:]
        
    def decode_base64_authorization_header(self, base64_authorization_header: str) -> str:
        if base64_authorization_header is None :
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            decoded_bytes = base64.b64decode(base64_authorization_header)
            return decoded_bytes.decode('utf-8')
        except Exception:
            return None
        
        
    def extract_user_credentials(self, decoded_base64_authorization_header: str) -> Tuple:
        if decoded_base64_authorization_header is None:
            return (None, None)
        if not isinstance(decoded_base64_authorization_header, str):
            return (None, None)
        if(":") in decoded_base64_authorization_header:
            splited_auth_header = decoded_base64_authorization_header.split(":")
            email = splited_auth_header[0]
            password = ":".join(splited_auth_header[1:])
            return (email, password)
    
    
    def user_object_from_credentials(self, user_email: str, user_pwd: str) -> Optional['User']:
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None
        useres = User.search({'email': user_email})
        
        if not useres:
            return None
        user = useres[0]
        
        if not user.is_valid_password(user_pwd):
            return None
        
        return user
        
        
    def current_user(self, request=None) -> user:
        user_auth_header = Auth.authorization_header(request)
        user_extraced_auth_header = self.extract_base64_authorization_header(user_auth_header)
        user_decoded_auth_header = self.decode_base64_authorization_header(user_extraced_auth_header)
        user_credentials = self.extract_user_credentials(user_decoded_auth_header)
        if user_credentials:
            user_email, user_pwd = user_credentials
            return self.user_object_from_credentials(user_email, user_pwd)
        return None
        