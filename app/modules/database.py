from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.configuration import Config


Base = declarative_base()
engine = create_engine(Config.DB_CONNECT_PATH)
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()

def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()
        