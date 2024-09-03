#!/usr/bin/env python3
""" Module of authentication """
from flask import request
from typing import List, TypeVar
from models.user import User


U = TypeVar('User')


class Auth:
    """ Auth class """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ require_auth method """
        if path is None or excluded_paths is None or len(excluded_paths) == 0:
            return True
        if path[-1] != '/':
            path_s = path + '/'
        if path[-1] == '/':
            path_s = path[:-1]
        if path in excluded_paths or path_s in excluded_paths:
            return False
        return True

    def authorization_header(self, request=None) -> str:
        """ authorization_header method """
        if request is None or request.headers.get('Authorization') is None:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> U:
        """ current_user method """
        return None
