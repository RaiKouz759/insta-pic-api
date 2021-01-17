from flask_restx import Resource, Namespace, fields
from flask import request, session
from .model import Post
from app import db
from flask_jwt_extended import (jwt_required, get_jwt_identity)
from .model import Post
from .schema import PostSchema
from app.User.model import User
from .constants import MAX_LATEST_POSTS
import json
import time

api = Namespace('Posts', description='API for getting and posting posts')

submitPost_model = api.model('Submit Response', {
    'msg' : fields.String,
    'caption' : fields.String,
    'user_id': fields.Integer
})
submitPost_fail = api.model('Submit fail', {
    'code': fields.String
})
submitPost_body = api.model('Resource', {
    'file': fields.Raw(required=True, description='Blob file of image'),
    'caption': fields.String(description='caption of post'),
    'userId': fields.Integer(required=True, description='User id of user who posted.')
})


@api.route('/submitPost')
class SubmitPost(Resource):
    @jwt_required
    @api.response(200, 'Success', submitPost_model)
    @api.response(400, 'Failure', submitPost_fail)
    @api.doc(body=submitPost_body)
    def post(self):
        ''' Receive a post from the client - auth token needed'''
        try:
            image = request.files.get('file')
            caption = request.form.get('caption')
            user_id = request.form.get('userId')
            if not image or not user_id: 
                # there should be a user or image for every post
                raise Exception
            # image_ext = request.files.get('file').name
            p = Post(image_file=image.read(), comment=caption, user_id=user_id)
            db.session.add(p)
            db.session.commit()

        except Exception as e:
            print(e)
            return {'code' : 'failed to post'}, 400
        
        return {'msg': 'successfully posted post', 'caption': caption, 
                'user_id': user_id}

@api.route('/id/<int:postId>', doc=False)
class GetPostId(Resource):
    def get(self, postId):
        ''' Get a single Post by its ID'''

        post = Post.query.get(postId)
        post_schema = PostSchema()
        if not post:
            return {'error' : 'post does not exist'}
        
        return post_schema.dump(post)

@api.route('/latest/<int:num_post>')
class GetLatestPosts(Resource):
    def get(self, num_post):
        ''' Get latest posts
            Return Json of posts'''
        if num_post > MAX_LATEST_POSTS or num_post < 1:
            return {'error' : f'maximum of {MAX_LATEST_POSTS} requests allowed.'}
        
        posts = Post.query.order_by(Post.datetime_posted.desc()).limit(num_post).all()
        posts_schema = PostSchema(many=True)
        if not posts:
            return {'error' : 'no posts exist'}

        return posts_schema.dump(posts)

@api.route('/subscribe')
class SubscribePost(Resource):
    @jwt_required
    def post(self):
        ''' For client to get updates
            client sends most up to date post id
            updates are sent back if available '''
        try:
            post_id = request.form.get('latestId')
            if not post_id:
                return {'error': 'no post id in subscription'}, 400
            post = Post.query.get(post_id)
            if not post:
                return {'error': 'no such post id'}, 400

            new_posts = Post.query.filter(Post.id > post_id).order_by(Post.id.asc()).all()
            if new_posts:
                post_schema = PostSchema(many=True)
                return post_schema.dump(new_posts)

            return {'error': 'no new posts'}, 502
        except Exception:
            return {'error': 'stop subscribing'}, 401


# @api.route('/testToken')
# class TestToken(Resource):
#     @jwt_required
#     def post(self):
#         return {'message': 'token authorized.'}

