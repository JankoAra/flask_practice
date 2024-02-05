# coding: utf-8
from sqlalchemy import CHAR, Column, DateTime, ForeignKey, String, text
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class DrugaTabela(Base):
    __tablename__ = 'drugaTabela'

    id = Column(INTEGER(11), primary_key=True)
    email = Column(String(45))

    def __init__(self, emailParam):
        self.email = emailParam


class PrvaTabela(Base):
    __tablename__ = 'prvaTabela'

    id = Column(INTEGER(11), primary_key=True)
    ime = Column(String(255))
    broj = Column(INTEGER(11))
    opis = Column(String(45))

    def __init__(self, imeParam, brojParam, opisParam):
        self.ime = imeParam
        self.broj = brojParam
        self.opis = opisParam


class User(Base):
    __tablename__ = 'users'

    id = Column(INTEGER(11), primary_key=True)
    email = Column(String(100), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    username = Column(String(45), nullable=False, unique=True)

    def __init__(self, emailParam, passwordParam, usernameParam):
        self.email = emailParam
        self.password = passwordParam
        self.username = usernameParam


class Poke(Base):
    __tablename__ = 'pokes'

    id = Column(INTEGER(11), primary_key=True)
    userPoking = Column(ForeignKey('users.id', onupdate='CASCADE'), nullable=False, index=True)
    userPoked = Column(ForeignKey('users.id', onupdate='CASCADE'), nullable=False, index=True)
    status = Column(CHAR(1), nullable=False)
    time = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))

    user = relationship('User', primaryjoin='Poke.userPoked == User.id')
    user1 = relationship('User', primaryjoin='Poke.userPoking == User.id')

    def __init__(self, userPokingParam, userPokedParam, statusParam):
        self.userPoking = userPokingParam
        self.userPoked = userPokedParam
        self.status = statusParam
