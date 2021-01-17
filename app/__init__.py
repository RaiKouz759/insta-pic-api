from flask import Flask, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_restx import Api
# from flask_cors import CORS
from flask_jwt_extended import JWTManager
from app.config import Config
from werkzeug.middleware.proxy_fix import ProxyFix

class MyApi(Api):
    @property
    def specs_url(self):
        """Monkey patch for HTTPS"""
        scheme = 'http' if '5000' in self.base_url else 'https'
        return url_for(self.endpoint('specs'), _external=True, _scheme=scheme)

db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate()
api = MyApi(doc='/api/doc')
jwt = JWTManager()

def create_app():
    # initialize the core application
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # proxy fix
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_port=1)

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




