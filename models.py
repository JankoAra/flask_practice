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


class TrecaTabela(Base):
    __tablename__ = 'trecaTabela'

    id = Column(INTEGER(11), primary_key=True)
    sadrzaj = Column(String(45))

    def __init__(self, sadrzajParam):
        self.sadrzaj = sadrzajParam
