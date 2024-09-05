#!/usr/bin/env python3
""" Module of Session expiration auth stored in data base """
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """ SessionDBAuth class """

    def create_session(self, user_id=None):
        """ Creates a Session ID for a user_id """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        session_dictionary = {
            "user_id": user_id,
            "session_id": session_id
        }
        user = UserSession(**session_dictionary)
        user.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """ Returns a User ID based on a Session ID """
        if session_id is None:
            return None
        user_id = UserSession.search({"session_id": session_id})[0].user_id
        if user_id:
            return user_id
        return None

    def destroy_session(self, request=None):
        """ Deletes the user session / logout """
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if session_id is None:
            return False
        try:
            session = UserSession.search({"session_id": session_id})[0]
            session.remove()
            return True
        except Exception:
            return False
