from flask import request
from typing import List, TypeVar
from models import user

User = TypeVar('User')

class Auth:
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        if not path:
            return True
        if excluded_paths == None or len(excluded_paths) == 0:
            return True
        normalize_path = path.rstrip('/')
        
        for excluded_path in excluded_paths:
            normalized_excluded_path = excluded_path.rstrip('/')
            
            if normalized_excluded_path.endswith("*"):
                if normalize_path.startswith(normalized_excluded_path[0:-1]):
                    return False
                
            else:
                if normalize_path == normalized_excluded_path:
                    return False
            
        return True
    
    
    def authorization_header(self, request=None) -> str:
        if request == None:
            return None
        
        auth_header = request.headers.get('Authorization')
        
        if auth_header:
            return auth_header
        else:
            return None
    
    
    def current_user(self, request=None) -> User:
        if request is None:
            return None