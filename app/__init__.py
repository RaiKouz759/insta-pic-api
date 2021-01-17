from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_restx import Api
# from flask_cors import CORS
from flask_jwt_extended import JWTManager
from app.config import Config

db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate()
api = Api()
jwt = JWTManager()

def create_app():
    # initialize the core application
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize Plugins
    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)
    api.init_app(app)
    jwt.init_app(app)

    # import models here so that they get migrated. 
    from app.Post.model import Post
    from app.User.model import User, RevokedToken

    #import routes and add namespace
    from app.Post.controller import api as post_api
    from app.User.controller import api as user_api
    api.add_namespace(post_api, '/api/post')
    api.add_namespace(user_api, '/api/user')

    #set cors headers
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
        return response

    return app




