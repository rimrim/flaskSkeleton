import os

from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt import JWT, JWTError
from security import authenticate, identity


from resources.item import Item, ItemList
from resources.store import Store, StoreList
from resources.user import UserRegister, User

app = Flask(__name__)

app.config['DEBUG'] = True

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# this help flask app see exceptions from flask-jwt
app.config['PROPAGATE_EXCEPTIONS'] = True
# this secret key is used to encode cookies
app.secret_key = 'some secret'
api = Api(app)

jwt = JWT(app, authenticate, identity)

api.add_resource(Store, '/store/<string:name>')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(StoreList, '/stores')
api.add_resource(UserRegister, '/register')
api.add_resource(User, '/user/<int:user_id>')

@app.errorhandler(JWTError)
def auth_error_handler(err):
    return jsonify({'message':'cannot authenticate, jwt invalid'}), 401

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
