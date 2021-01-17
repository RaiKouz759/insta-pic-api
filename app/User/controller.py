from flask_restx import Resource, Namespace
from .schema import LoginSchema, RegisterSchema
from flask import request, jsonify
from marshmallow import ValidationError
from .model import User, RevokedToken
from app import db
from flask_jwt_extended import (create_access_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)
import datetime
from .constants import JWT_EXPIRY_TIME

api = Namespace('Users', description='API for user access and endpoints')    

def format_message(message, subtitle='message'):
    return {subtitle : message}

@api.route('/register')
class UserRegistration(Resource):
    def post(self):
        body = request.json
        try:
            # load the body into schema to do input validation
            credentials = RegisterSchema().load(body)

            # check for existing users
            if User.find_by_username(credentials['username']):
                return {'message' : 'User {} already exists.'.format(credentials['username'])}, 401

            new_user = User(
                username = credentials['username'],
                password = User.generate_hash(credentials['password'])
            )
            # verify that user can be created
            try:
                db.session.add(new_user)
                db.session.commit()
                access_token = create_access_token(identity = credentials['username'], expires_delta=datetime.timedelta(seconds=JWT_EXPIRY_TIME))
                return {
                    'user' : {'username': new_user.username, 'user_id': new_user.id},
                    'token': access_token
                    }
            except:
                return {'message': 'Something went wrong'}, 500

        except Exception as err:
            return jsonify(err.messages)
        
        # return {'message': 'User registration', 'credentials': credentials}

@api.route('/login')
class UserLogin(Resource):
    def post(self):
        body = request.json
        print(body)
        try:
            # load the body into schema to do input validation
            credentials = LoginSchema().load(body)
            current_user = User.find_by_username(credentials['username'])

            # check if user exists
            if not current_user:
                return format_message('User {} does not exist'.format(credentials['username'])), 401
            # validate password
            if User.verify_hash(credentials['password'], current_user.password): 
                access_token = create_access_token(identity = credentials['username'], expires_delta=datetime.timedelta(seconds=JWT_EXPIRY_TIME))
                return {'user' : {'username': current_user.username, 'user_id': current_user.id},
                        'token': access_token
                        }
            else:
                return format_message('Wrong credentials'), 401

        except Exception as err:
            return jsonify(err.messages)

      
@api.route('/users')
class AllUsers(Resource):
    def get(self):
        return {'message': 'List of users'}

    def delete(self):
        return {'message': 'Delete all users'}


@api.route('/getUsername')
class UserUsername(Resource):
    @jwt_required
    def get(self):
        current_user = get_jwt_identity()
        return {
            'user': current_user
        }
      