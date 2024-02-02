# coding: utf-8
from sqlalchemy import Column, String
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class DrugaTabela(Base):
    __tablename__ = 'drugaTabela'

    id = Column(INTEGER(11), primary_key=True)
    email = Column(String(45))

    def __init__(self, id, email):
        self.id = id, self.email = email


class PrvaTabela(Base):
    __tablename__ = 'prvaTabela'

    id = Column(INTEGER(11), primary_key=True)
    ime = Column(String(255))
    broj = Column(INTEGER(11))

    def __init__(self, id, ime, broj):
        self.id = id, self.ime = ime, self.broj = broj
