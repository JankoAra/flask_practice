from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(45), nullable=False, unique=True)

    def __init__(self, emailParam, passwordParam, usernameParam):
        self.email = emailParam
        self.password = passwordParam
        self.username = usernameParam

class Poke(db.Model):
    __tablename__ = 'pokes'

    id = db.Column(db.Integer, primary_key=True)
    userPoking = db.Column(db.ForeignKey('users.id', onupdate='CASCADE'), nullable=False, index=True)
    userPoked = db.Column(db.ForeignKey('users.id', onupdate='CASCADE'), nullable=False, index=True)
    status = db.Column(db.CHAR(1), nullable=False)
    time = db.Column(db.DateTime, nullable=False, server_default=db.text("current_timestamp()"))

    user = db.relationship('User', primaryjoin='Poke.userPoked == User.id')
    user1 = db.relationship('User', primaryjoin='Poke.userPoking == User.id')

    def __init__(self, userPokingParam, userPokedParam, statusParam):
        self.userPoking = userPokingParam
        self.userPoked = userPokedParam
        self.status = statusParam