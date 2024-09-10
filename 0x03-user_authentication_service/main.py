#!/usr/bin/env python3
"""
Main file
Was easier than unittests
"""
import requests
# from db import DB
# from user import User
# from sqlalchemy.exc import InvalidRequestError
# from sqlalchemy.orm.exc import NoResultFound
# from auth import Auth
# from auth import _hash_password


def register_user(email: str, password: str) -> None:
    """ Register user """
    response = requests.post("http://0.0.0.0:5000/users",
                             data={"email": email, "password": password})
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "user created"}


def log_in_wrong_password(email: str, password: str) -> None:
    """ Log in with wrong password """
    response = requests.post("http://0.0.0.0:5000/sessions",
                             data={"email": email, "password": password})
    assert response.status_code == 401
    assert response.reason == "UNAUTHORIZED"


def log_in(email: str, password: str) -> str:
    """ Log in """
    response = requests.post("http://0.0.0.0:5000/sessions",
                             data={"email": email, "password": password})
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "logged in"}
    return response.cookies.get("session_id")


def profile_unlogged() -> None:
    """ Profile unlogged """
    response = requests.get("http://0.0.0.0:5000/profile")
    assert response.status_code == 403
    assert response.reason == "FORBIDDEN"


def profile_logged(session_id: str) -> None:
    """ Profile logged """
    response = requests.get("http://0.0.0.0:5000/profile",
                            cookies={"session_id": session_id})
    assert response.status_code == 200
    assert response.json() == {"email": "guillaume@holberton.io"}


def log_out(session_id: str) -> None:
    """ Log out """
    response = requests.delete("http://0.0.0.0:5000/sessions",
                               cookies={"session_id": session_id})
    assert response.status_code == 200
    assert response.url == "http://0.0.0.0:5000/"


def reset_password_token(email: str) -> str:
    """ Reset password token """
    response = requests.post("http://0.0.0.0:5000/reset_password",
                             data={"email": email})
    assert response.status_code == 200
    assert response.json().get("email") == email
    return response.json().get("reset_token")


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """ Update password """
    response = requests.put("http://0.0.0.0:5000/reset_password",
                            data={"email": email,
                                  "reset_token": reset_token,
                                  "new_password": new_password})
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "Password updated"}


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)


# ##########################################################################
""" Main tests for tasks """

# my_db = DB()

# user_1 = my_db.add_user("test@test.com", "SuperHashedPwd")
# print(user_1.id)

# user_2 = my_db.add_user("test1@test.com", "SuperHashedPwd1")
# print(user_2.id)


# ##########################################################################


# my_db = DB()

# user = my_db.add_user("test@test.com", "PwdHashed")
# print(user.id)

# find_user = my_db.find_user_by(email="test@test.com")
# print(find_user.id)

# try:
#     find_user = my_db.find_user_by(email="test2@test.com")
#     print(find_user.id)
# except NoResultFound:
#     print("Not found")

# try:
#     find_user = my_db.find_user_by(no_email="test@test.com")
#     print(find_user.id)
# except InvalidRequestError:
#     print("Invalid")


# ##########################################################################


# my_db = DB()

# email = "test@test.com"
# hashed_password = "hashedPwd"

# user = my_db.add_user(email, hashed_password)
# print(user.id)

# try:
#     my_db.update_user(user.id, hashed_password="NewPwd")
#     print("Password updated")
# except ValueError:
#     print("Error")


# ##########################################################################


# print(_hash_password("Hello Holberton"))


# ##########################################################################


# email = "me@me.com"
# password = "mySecuredPwd"

# auth = Auth()

# try:
#     user = auth.register_user(email, password)
#     print("successfully created a new user!")
# except ValueError as err:
#     print("could not create a new user: {}".format(err))

# try:
#     user = auth.register_user(email, password)
#     print("successfully created a new user!")
# except ValueError as err:
#     print("could not create a new user: {}".format(err))


# ##########################################################################


# email = "bob@bob.com"
# password = "MyPwdOfBob"
# auth = Auth()

# auth.register_user(email, password)

# print(auth.valid_login(email, password))

# print(auth.valid_login(email, "WrongPwd"))

# print(auth.valid_login("unknown@email", password))


# ##########################################################################


# email = "bob@bob.com"
# password = "MyPwdOfBob"
# auth = Auth()

# auth.register_user(email, password)

# print(auth.create_session(email))
# print(auth.create_session("unknown@email.com"))
