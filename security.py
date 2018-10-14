"""
This file provide boilerplate helpers for flask-jwt
"""
from werkzeug.security import safe_str_cmp
from models.user import UserModel

def authenticate(username, password):
    """
    This function called when a user calls /auth, it stay here bc we use flask-jwt
    :param username:
    :param password:
    :return: a user if auth success, none otherwise
    """
    user = UserModel.find_by_username(username)
    if user and safe_str_cmp(user.password, password):
        return user

def identity(payload):
    """
    called when user is authenticated (Flask-jwt already verify the jwt token is correct)
    :param payload: a dictionary with identity as a key, user id
    :return:
    """
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)
