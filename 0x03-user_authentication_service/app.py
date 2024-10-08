#!/usr/bin/env python3
"""app mofule"""
from typing import Tuple, Union
from flask import Flask, jsonify, abort, request, redirect
from auth import Auth

app = Flask(__name__)

AUTH = Auth()


@app.route('/', methods=['GET'], strict_slashes=False)
def index() -> str:
    """index function

    Returns:
        str: welcome message
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'])
def register_user() -> Tuple[str, int]:
    """register user function

    Returns:
        Tuple[str, int]: email and status code
    """
    email = request.form.get('email')
    password = request.form.get('password')

    try:
        user = AUTH.register_user(email, password)
    except ValueError:
        return jsonify({"message": "email already registered"}), 400

    response = {"email": email, "message": "user created"}
    return jsonify(response)


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login() -> str:
    """login function

    Returns:
        str: user email
    """
    email = request.form.get('email')
    password = request.form.get('password')
    valid_login = AUTH.valid_login(email, password)

    if not valid_login:
        abort(401)

    session_id = AUTH.create_session(email)
    response = jsonify({'email': email, 'message': 'logged in'})
    response.set_cookie('session_id', session_id)
    return response


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout() -> Union[abort, redirect]:
    """logout function

    Returns:
        Union[abort, redirect]: redirect to /
    """
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)

    if session_id is None or user is None:
        abort(403)

    AUTH.destroy_session(user.id)
    return redirect('/')


@app.route('/profile', strict_slashes=False)
def profile() -> str:
    """profile function

    Returns:
        str: user email
    """
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)

    if session_id is None or user is None:
        abort(403)

    return jsonify({'email': user.email})


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_reset_password_token() -> str:
    """get reset password token

    Returns:
        str: reset token
    """
    try:
        email = request.form.get('email')
        reset_token = AUTH.get_reset_password_token(email)
    except ValueError:
        abort(403)

    return jsonify({"email": email, "reset_token": reset_token})


@app.route('/reset_password', methods=['PUT'], strict_slashes=False)
def update_password() -> Tuple[str, int]:
    """update password

    Returns:
        Tuple[str, int]: email and message
    """
    reset_token = request.form.get('reset_token')
    new_password = request.form.get('new_password')
    email = request.form.get('email')
    try:
        AUTH.update_password(reset_token, new_password)
    except Exception:
        abort(403)

    return jsonify({"email": email, "message": "Password updated"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
