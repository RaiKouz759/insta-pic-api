from marshmallow import Schema, fields
from app.User.model import User
import base64

class PostSchema(Schema):
    id = fields.Int()
    imageString = fields.Method('get_encoded_image_string')
    caption = fields.Str(attribute='comment')
    userId = fields.Int(attribute='user_id')
    datetimePosted = fields.Method('get_string_datetime')
    username = fields.Method('get_username')

    def get_encoded_image_string(self, obj):
        if not obj.image_file:
            return None
        return base64.b64encode(obj.image_file).decode()

    def get_string_datetime(self, obj):
        if not obj.datetime_posted:
            return None
        return str(obj.datetime_posted)

    def get_username(self, obj):
        if not obj.user_id:
            return None
        username = User.query.get(obj.user_id).username
        if not username:
            return None
        return username