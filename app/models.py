from werkzeug.security import generate_password_hash, check_password_hash

from app import db, current_app
from datetime import datetime
from flask_login import UserMixin
from app import login
from hashlib import md5
import jwt
from time import time

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

#关注者关联表
followers = db.Table(
    'followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),#粉丝
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))#关注
)


class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.String(24), index=True, unique=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    seats= db.relationship('seats', backref='use', lazy='dynamic')
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    image_name = db.Column(db.String(30), index=True)
    user_image = db.Column(db.String(2048), index=True)
    facedata = db.Column(db.String(2048), index=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return self.followed.filter(followers.c.followed_id==user.id).count()>0

    def followed_posts(self):
        followed = Post.query.join(followers, (followers.c.followed_id == Post.user_id)).filter(followers.c.follower_id == self.id)
        own = Post.query.filter_by(user_id=self.id)
        return followed.union(own).order_by(Post.timestamp.desc())

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'], algorithm='HS256').encode('utf-8').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)

    followed = db.relationship(
        'User',
        secondary=followers,
        primaryjoin=(followers.c.follower_id==id),
        secondaryjoin=(followers.c.followed_id==id),
        backref=db.backref('followers', lazy='dynamic'),
        lazy='dynamic'
    )

    def __repr__(self):
        return '<User {}>'.format(self.username)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    language = db.Column(db.String(5))
    def __repr__(self):
        return '<Post {}'.format(self.body)

class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_name = db.Column(db.String(30), index=True)
    bookimage = db.Column(db.String(2048), index=True)
    bookname = db.Column(db.String(64), index=True, unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return '<Books {}'.format(self.bookname)

class Studyrooms(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    roomname = db.Column(db.String(64), index=True, unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    seats= db.relationship('seats', backref='thein', lazy='dynamic')
    def __repr__(self):
        return '<Studyrooms {}'.format(self.roomname)

class seats(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    seatid = db.Column(db.String(64), index=True, unique=True)
    state =db.Column(db.Integer,    index=True, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    room_id = db.Column(db.Integer, db.ForeignKey('studyrooms.id'))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return '<seats {}'.format(self.state)