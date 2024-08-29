#!/usr/bin/env python3
""" Password hashing """


import bcrypt


def hash_password(password: str) -> bytes:
    """ Hash a password for storing """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password


def is_valid(hashed_password: bytes, password: str) -> bool:
    """ Validate a password with its hashed version """
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
