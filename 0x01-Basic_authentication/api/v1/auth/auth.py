#!/usr/bin/env python3
""" Module of authentication """
from flask import request
from typing import List, TypeVar
from models.user import User


User = TypeVar('User')


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
        return None

    def current_user(self, request=None) -> User:
        """ current_user method """
        return None
