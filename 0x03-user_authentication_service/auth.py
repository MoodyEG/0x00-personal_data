#!/usr/bin/env python3
""" Auth module """
import bcrypt
from db import DB
from user import User
# from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """ Hash password """
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt)


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """ Register user """
        try:
            self._db.find_user_by(email=email)
            raise ValueError(
                "User {} already exists".format(email))
        except NoResultFound:
            hashed_password = _hash_password(password)
            return self._db.add_user(email, hashed_password)

    def valid_login(self, email: str, password: str) -> bool:
        """ Validate login """
        user = self._db.find_user_by(email=email)
        if user is None:
            return False
        return bcrypt.checkpw(password.encode('utf-8'), user.hashed_password)
