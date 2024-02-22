#!/usr/bin/env python3
'''
    The main module.
'''
import requests


URL = 'http://127.0.0.1:5000'


def register_user(email: str, password: str) -> None:
    '''
        register_user: function
        @email: Email to register.
        @password: Password for the user.
        return: None
    '''
    requests.post(URL + '/users', data={"email": email, "password": password})


def log_in_wrong_password(email: str, password: str) -> None:
    '''
        log_in_wrong_password: function
        @email: Email to check.
        @password: Password to check.
        return: None.
    '''
    data_payload = {"email": email, "password": password}
    res = requests.post(URL + '/sessions', data=data_payload)
    assert res.status_code == 401


def log_in(email: str, password: str) -> str:
    '''
        log_in: function
        @email: Email to check.
        @password: Password to check.
        return: Response of the login.
    '''
    data_payload = {"email": email, "password": password}
    res = requests.post(URL + '/sessions', data=data_payload)
    assert res.status_code == 200
    assert res.json() == {"email": email, "message": "logged in"}
    assert res.cookies.get("session_id")


def profile_unlogged() -> None:
    '''
        profile_unlogged: function.
        return: None
    '''
    res = requests.get(URL + '/profile')
    assert res.status_code == 403


def profile_logged(session_id: str) -> None:
    '''
        profile_logged: function.
        @session_id: Session ID.
        return: None
    '''
    res = requests.get(URL + '/profile')
    assert res.status_code == 200
    assert "email" in res.json()
    assert res.cookies.get("session_id")


def log_out(session_id: str) -> None:
    '''
        log_out: function.
        @session_id: Session ID.
        return: None
    '''
    res = requests.delete(URL + '/sessions')
    assert res.status_code == 200
    assert res.json() == {"message": "Bienvenue"}
    assert res.cookies.get("session_id")


def reset_password_token(email: str) -> str:
    '''
        reset_password_token: function
        @email: Email to check.
        return: Response.
    '''
    data_payload = {"email": email}
    final_url = URL + '/reset_password'
    res = requests.post(final_url, data=data_payload)
    assert res.status_code == 200
    assert "email" in res.json()
    assert "reset_token" in res.json()
    return res.json().get('reset_token')


def update_password(email: str, reset_token: str, new_password: str) -> None:
    '''
        update_password: function
        @email: Email to check.
        @reset_token: Reset token.
        @new_password: New Password.
        return: None
    '''
    data_payload = {
                "email": email,
                "reset_token": reset_token,
                "new_password": new_password
    }
    final_url = URL + '/reset_password'
    res = requests.put(final_url, data=data_payload)
    assert res.status_code == 200
    assert res.json() == {"email": email, "message": "Password updated"}


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
