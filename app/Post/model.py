from app import db
from datetime import datetime

class Post(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    image_file = db.Column(db.Binary)
    comment = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    datetime_posted = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return f'<Post> {self.id} by <User> {self.user_id}'

    