from extensions import db


class Users(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(45), nullable=False, unique=True)
    profileImagePath = db.Column(db.Text)
    image = db.Column(db.LargeBinary(length=(2**32)-1))

    posts = db.relationship('Posts', backref='author', lazy=True)

    def __init__(self, emailParam, passwordParam, usernameParam):
        self.email = emailParam
        self.password = passwordParam
        self.username = usernameParam

    def to_dict(self):
        d = {
            "id": self.id,
            "username": self.username
        }
        return d


class Pokes(db.Model):
    __tablename__ = 'pokes'

    id = db.Column(db.Integer, primary_key=True)
    userPoking = db.Column(db.ForeignKey('users.id', onupdate='CASCADE'), nullable=False, index=True)
    userPoked = db.Column(db.ForeignKey('users.id', onupdate='CASCADE'), nullable=False, index=True)
    status = db.Column(db.CHAR(1), nullable=False)
    datetime = db.Column(db.DateTime, nullable=False, server_default=db.text("current_timestamp()"))

    user = db.relationship('Users', primaryjoin='Pokes.userPoked == Users.id')
    user1 = db.relationship('Users', primaryjoin='Pokes.userPoking == Users.id')

    def __init__(self, userPokingParam, userPokedParam, statusParam):
        self.userPoking = userPokingParam
        self.userPoked = userPokedParam
        self.status = statusParam

    def to_dict(self):
        d = {
            "id": self.id,
            "userPoking": self.user1.to_dict(),
            "userPoked": self.user.to_dict(),
            "status": self.status,
            "datetime": self.datetime
        }
        return d


class Posts(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(500), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id', onupdate='CASCADE'), nullable=False)
    datetime = db.Column(db.DateTime, server_default=db.text("current_timestamp()"))

    likes = db.relationship('Likes', backref='post', lazy='joined')

    def __init__(self, authorID, content):
        self.author_id = authorID
        self.content = content

    def to_dict(self):
        d = {
            "id": self.id,
            "content": self.content,
            "author": self.author.to_dict(),
            "datetime": self.datetime,
            "likes": [like.to_dict() for like in self.likes],
            "numOfLikes": len(self.likes)
        }
        return d


class Likes(db.Model):
    __tablename__ = 'likes'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id', onupdate='CASCADE'), primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id', onupdate='CASCADE'), primary_key=True)

    user = db.relationship('Users', primaryjoin='Likes.user_id == Users.id')

    # post = db.relationship('Posts', primaryjoin='Likes.post_id == Posts.id')

    def __init__(self, user_id, post_id):
        self.user_id = user_id
        self.post_id = post_id

    def to_dict(self):
        d = {
            "user": self.user.to_dict()
            # , "post": self.post.to_dict()
        }
        return d
