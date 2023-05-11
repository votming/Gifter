from sqlalchemy import ForeignKey, Column, String, Integer, Text, SmallInteger, DateTime
from sqlalchemy import func
from sqlalchemy.orm import relationship

from app.utils.mixins import DBOperationsMixin
from app.modules.database import Base


class Role(DBOperationsMixin, Base):
    __tablename__ = 'user_roles'

    id = Column("id", Integer, primary_key=True)
    name = Column('name', String(120))
    created_at = Column(DateTime(timezone=False), server_default=func.now())
    updated_at = Column(DateTime(timezone=False), onupdate=func.now())

    def __init__(self, name='none'):
        self.name = name


class User(DBOperationsMixin, Base):
    __tablename__ = 'users'

    id = Column("id", Integer, primary_key=True)
    login = Column('login', String)
    password = Column('password', String)
    role_id = Column('role_id', Integer, ForeignKey("user_roles.id"))
    role = relationship("Role", backref="users")
    created_at = Column(DateTime(timezone=False), server_default=func.now())
    updated_at = Column(DateTime(timezone=False), onupdate=func.now())

    def __init__(self, login='default', password=None, role_id=None):
        self.login = login
        self.password = password
        self.role_id = role_id


class Currency(DBOperationsMixin, Base):
    __tablename__ = 'currencies'

    id = Column("id", Integer, primary_key=True)
    name = Column('name', String)
    name_en = Column('name_en', String)
    code = Column('code', String(5))
    symbol = Column('symbol', String(5))
    created_at = Column(DateTime(timezone=False), server_default=func.now())
    updated_at = Column(DateTime(timezone=False), onupdate=func.now())

    def __init__(self, name='default', name_en='default', code=None, symbol=None):
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
    created_at = Column(DateTime(timezone=False), server_default=func.now())
    updated_at = Column(DateTime(timezone=False), onupdate=func.now())

    def __init__(self, name='', code='__', demonym='', demonym_plural='', bank_name='', currency_id=None):
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
    created_at = Column(DateTime(timezone=False), server_default=func.now())
    updated_at = Column(DateTime(timezone=False), onupdate=func.now())

    def __init__(self, name='default', code=None):
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
    created_at = Column(DateTime(timezone=False), server_default=func.now())
    updated_at = Column(DateTime(timezone=False), onupdate=func.now())

    def __init__(self, template='none', language_id=None, country_id=None, gender=True):
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
    created_at = Column(DateTime(timezone=False), server_default=func.now())
    updated_at = Column(DateTime(timezone=False), onupdate=func.now())

    def __init__(self, template='none', language_id=None, country_id=None, number=1):
        self.template = template
        self.number = number
        self.language_id = language_id
        self.country_id = country_id
