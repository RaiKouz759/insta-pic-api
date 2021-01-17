from flask import jsonify

BASE_ROUTE = 'users'

def register_routes(api, app, root='api'):
    from .controller import api as user_api

    api.add_namespace(user_api, path=f'/{root}/{BASE_ROUTE}')

from app import jwt
from .model import RevokedToken


# jwt blacklisting the expired tokens
@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return RevokedToken.is_jti_blacklisted(jti)

@jwt.expired_token_loader
def my_expired_token_callback(expired_token):
    token_type = expired_token['type']
    return jsonify({
        'status': 401,
        'sub_status': 42,
        'msg': 'The {} token has expired'.format(token_type)
    }), 401




