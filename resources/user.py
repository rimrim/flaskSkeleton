from flask_restful import Resource, reqparse
from werkzeug.security import safe_str_cmp
from models.user import UserModel
from flask_jwt_extended import (create_access_token, create_refresh_token)


_user_parser = reqparse.RequestParser()
_user_parser.add_argument(
    'username',
    type=str,
    required=True,
    help='This field cannot be blank'
)
_user_parser.add_argument(
    'password',
    type=str,
    required=True,
    help='This field cannot be blank'
)

class UserRegister(Resource):
    """
    This class allow user to register by sending a post request including username/password
    """

    def post(self):
        data = _user_parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {'message':'username already exist'}, 400

        user = UserModel(**data)
        user.save_to_db()

        return {'message':'User created successfully'}, 201

class User(Resource):
    @classmethod
    def get(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': 'user not found'}, 404
        return user.json()

    @classmethod
    def delete(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': 'user not found'}, 404
        user.delete_from_db()
        return {'message': 'user deleted'}

class UserLogin(Resource):
    def post(self):
        # get data from parser
        data = _user_parser.parse_args()
        # find user in the db
        user = UserModel.find_by_username(data['username'])
        # check password
        # create access token
        # create refresh token
        if user and safe_str_cmp(user.password, data['password']):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(identity=user.id)
        # return them
            return {'access_token':access_token,
                    'refresh_token': refresh_token}, 200

        return {'message':'invalid credentials'}, 401

