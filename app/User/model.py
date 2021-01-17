from app import db
from passlib.hash import pbkdf2_sha256 as sha256


class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    # backref points to the one in this one-to-many relationship.
    posts = db.relationship('Post', backref='user', lazy='dynamic')

    def __repr__(self):
        return 'ID - {}, USER - {}'.format(self.id, self.username)

    @staticmethod
    def find_by_username(username):

        return User.query.filter_by(username=username).first()
    
    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)
    
    @staticmethod
    def verify_hash(password, pass_hash):
        return sha256.verify(password, pass_hash)

class RevokedToken(db.Model):
    __tablename__ = 'revoked_tokens'

    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(120))

    @staticmethod
    def is_jti_blacklisted(jti):
        query = RevokedToken.query.filter_by(jti=jti).first()
        return bool(query)
