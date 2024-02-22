#!/usr/bin/env python3
'''
    The app module.
'''
from flask import Flask, abort, jsonify, request
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
    AUTH.create_session(email)
    return jsonify({"email": email, "message": "logged in"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
