from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Users(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(45), nullable=False, unique=True)

    posts = db.relationship('Posts', backref='author', lazy=True)

    def __init__(self, emailParam, passwordParam, usernameParam):
        self.email = emailParam
        self.password = passwordParam
        self.username = usernameParam


class Pokes(db.Model):
    __tablename__ = 'pokes'

    id = db.Column(db.Integer, primary_key=True)
    userPoking = db.Column(db.ForeignKey('users.id', onupdate='CASCADE'), nullable=False, index=True)
    userPoked = db.Column(db.ForeignKey('users.id', onupdate='CASCADE'), nullable=False, index=True)
    status = db.Column(db.CHAR(1), nullable=False)
    time = db.Column(db.DateTime, nullable=False, server_default=db.text("current_timestamp()"))

    user = db.relationship('Users', primaryjoin='Pokes.userPoked == Users.id')
    user1 = db.relationship('Users', primaryjoin='Pokes.userPoking == Users.id')

    def __init__(self, userPokingParam, userPokedParam, statusParam):
        self.userPoking = userPokingParam
        self.userPoked = userPokedParam
        self.status = statusParam


class Posts(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(500), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id', onupdate='CASCADE'), nullable=False)
    datetime = db.Column(db.DateTime, server_default=db.text("current_timestamp()"))

    def __init__(self, authorID, content):
        self.author_id = authorID
        self.content = content