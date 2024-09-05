#!/usr/bin/env python3
""" Module of Session expiration authentication """
from api.v1.auth.session_auth import SessionAuth
import uuid
import os
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """ SessionExpAuth class """
    def __init__(self):
        """ Initialzation of the class """
        self.session_duration = int(os.getenv("SESSION_DURATION", 0))

    def create_session(self, user_id=None):
        """ Creates a Session ID for a user_id """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        session_dictionary = {
            "user_id": user_id,
            "created_at": datetime.now()
        }
        self.user_id_by_session_id[session_id] = session_dictionary
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """ Returns a User ID based on a Session ID """
        if session_id is None:
            return None
        session_dict = self.user_id_by_session_id.get(session_id)
        if session_dict is None:
            return None
        user_id = session_dict.get("user_id")
        if self.session_duration <= 0:
            return user_id
        try:
            created_at = session_dict.get("created_at")
        except Exception:
            return None
        if created_at + timedelta(seconds=int(self.session_duration))\
           < datetime.now():
            return None
        return user_id
