from sqlalchemy import ForeignKey, Column, String, Integer, Text, SmallInteger
from sqlalchemy.orm import relationship

from app.utils.mixins import DBOperationsMixin
from app.modules.database import Base


class Currency(DBOperationsMixin, Base):
    __tablename__ = 'currencies'

    id = Column("id", Integer, primary_key=True)
    name = Column('name', String)
    name_en = Column('name_en', String)
    code = Column('code', String(5))
    symbol = Column('symbol', String(5))

    def __init__(self, name, name_en, code, symbol):
        self.name = name
        self.name_en = name_en
        self.code = code
        self.symbol = symbol


class Country(DBOperationsMixin, Base):
    __tablename__ = 'countries'

    id = Column("id", Integer, primary_key=True)
    name = Column('name', String)
    code = Column('code', String(2))
    demonym = Column('demonym', String)
    demonym_plural = Column('demonym_plural', String)
    bank_name = Column('bank_name', String)
    currency_id = Column('currency_id', Integer, ForeignKey("currencies.id"))
    currency = relationship("Currency", backref="countries")

    def __init__(self, name, code, demonym='', demonym_plural='', bank_name='', currency_id=None):
        self.name = name
        self.code = code
        self.demonym = demonym
        self.demonym_plural = demonym_plural
        self.bank_name = bank_name
        self.currency_id = currency_id


class Language(DBOperationsMixin, Base):
    __tablename__ = 'languages'

    id = Column("id", Integer, primary_key=True)
    name = Column('name', String)
    code = Column('code', String(3))

    def __init__(self, name, code):
        self.name = name
        self.code = code


class Title(DBOperationsMixin, Base):
    __tablename__ = 'titles'

    id = Column("id", Integer, primary_key=True)
    template = Column('template', Text)
    gender = Column('gender', String(10), nullable=True)
    language_id = Column('language_id', Integer, ForeignKey("languages.id"))
    country_id = Column('country_id', Integer, ForeignKey("countries.id"), nullable=True)
    language = relationship("Language", backref="titles")
    country = relationship("Country", backref="titles")

    def __init__(self, template, language_id, country_id, gender=True):
        self.template = template
        self.gender = gender
        self.language_id = language_id
        self.country_id = country_id


class Paragraph(DBOperationsMixin, Base):
    __tablename__ = 'paragraphs'

    id = Column("id", Integer, primary_key=True)
    number = Column('number', SmallInteger, default=1)
    template = Column('template', Text)
    language_id = Column('language_id', Integer, ForeignKey("languages.id"))
    country_id = Column('country_id', Integer, ForeignKey("countries.id"), nullable=True)
    language = relationship("Language", backref="paragraphs")
    country = relationship("Country", backref="paragraphs")

    def __init__(self, template, language_id, country_id=None, number=1):
        self.template = template
        self.number = number
        self.language_id = language_id
        self.country_id = country_id
