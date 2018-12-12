import os

from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from blacklist import BLACKLIST
from resources.item import Item, ItemList
from resources.store import Store, StoreList
from resources.user import UserRegister, User, UserLogin, UserLogout

app = Flask(__name__)

app.config['DEBUG'] = True

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# this help flask app see exceptions from flask-jwt
app.config['PROPAGATE_EXCEPTIONS'] = True
# this secret key is used to encode cookies, jwt
app.secret_key = 'some secret'
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
api = Api(app)

jwt = JWTManager(app)


@jwt.token_in_blacklist_loader
def check_if_token_in_black_list(decoded_token):
    return decoded_token['jti'] in BLACKLIST

@jwt.expired_token_loader
def token_expired():
    return jsonify({
        'message':'token expired'
    }), 401

@jwt.invalid_token_loader
def token_invalid():
    return jsonify({
        'message': 'token invalid'
    }), 401

@jwt.revoked_token_loader
def token_blacklisted():
    return jsonify({
        'message': 'token revoked'
    }), 401

@jwt.user_claims_loader
def add_admin_claims(identity):
    if identity == 1:
        return {'is_admin': True}
    return {'is_admin': False}

api.add_resource(Store, '/store/<string:name>')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(StoreList, '/stores')
api.add_resource(UserRegister, '/register')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserLogin, '/auth')
api.add_resource(UserLogout, '/logout')

# @app.errorhandler(JWTError)
# def auth_error_handler(err):
#     return jsonify({'message':'cannot authenticate, jwt invalid'}), 401

@app.route('/')
def hello_world():
  return 'hello world from docker-compose'

if __name__ == '__main__':
    from db import db

    db.init_app(app)

    if app.config['DEBUG']:
        @app.before_first_request
        def create_tables():
            db.create_all()

    app.run(host='0.0.0.0', port=5000)
