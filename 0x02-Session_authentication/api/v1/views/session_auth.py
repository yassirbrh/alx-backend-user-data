#!/usr/bin/env python3
'''
    Module of Session authentication views
'''
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User
from os import getenv


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login():
    '''
        login: function
        return: None
    '''
    email = request.form.get("email")
    if not email:
        return jsonify({"error": "email missing"}), 400
    password = request.form.get("password")
    if not password:
        return jsonify({"error": "password missing"}), 400
    try:
        users = User.search({'email': email})
    except Exception:
        return jsonify({"error": "no user found for this email"}), 404
    if not users:
        return jsonify({"error": "no user found for this email"}), 404
    for user in users:
        if not user.is_valid_password(password):
            return jsonify({"error": "wrong password"}), 401
    from api.v1.app import auth
    user = users[0]
    session_id = auth.create_session(user.id)
    SESSION_NAME = getenv("SESSION_NAME")
    user_dict = jsonify(user.to_json())
    user_dict.set_cookie(SESSION_NAME, session_id)
    return user_dict
