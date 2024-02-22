#!/usr/bin/env python3
'''
    The app module.
'''
from flask import Flask, abort, jsonify, redirect, request
from auth import Auth


app = Flask(__name__)
AUTH = Auth()


@app.route("/", methods=['GET'])
def main_page() -> dict:
    '''
        main_page: function
        return: JSON payload.
    '''
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=['POST'])
def users() -> dict:
    '''
        users: function
        return: JSON payload.
    '''
    email = request.form.get("email")
    password = request.form.get("password")
    try:
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=['POST'])
def login() -> dict:
    '''
        login: function
        return: JSON payload.
    '''
    email = request.form.get("email")
    password = request.form.get("password")
    if not AUTH.valid_login(email, password):
        abort(401)
    session_id = AUTH.create_session(email)
    resp = jsonify({"email": email, "message": "logged in"})
    resp.set_cookie("session_id", session_id)
    return resp


@app.route("/sessions", methods=["DELETE"])
def logout() -> str:
    '''
        logout: function
        return: Redirection to /
    '''
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect('/')


@app.route("/profile", methods=['GET'])
def profile() -> dict:
    '''
        profile: function
        return: JSON Payload.
    '''
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
    return jsonify({"email": user.email}), 200


@app.route("/reset_password", methods=['POST'])
def get_reset_password_token() -> dict:
    '''
        get_reset_password_token: function.
        return: JSON Payload.
    '''
    email = request.form.get("email")
    try:
        token = AUTH.get_reset_password_token(email)
    except ValueError:
        abort(403)
    return jsonify({"email": email, "reset_token": token}), 200


@app.route("/reset_password", methods=['PUT'])
def update_password() -> dict:
    '''
        update_password: function
        return: JSON Payload.
    '''
    email = request.form.get("email")
    reset_token = request.form.get("reset_token")
    new_password = request.form.get("new_password")
    try:
        token = AUTH.update_password(reset_token, new_password)
    except ValueError:
        abort(403)
    return jsonify({"email": email, "message": "Password updated"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
