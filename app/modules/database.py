import redis
import pickle
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.configuration import Config

# Declaration on the DB instance
Base = declarative_base()
engine = create_engine(Config.DB_CONNECT_PATH, pool_size=100, max_overflow=10)
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, password=Config.REDIS_PASSWORD)


def get_db():
    """
    Context manager for providing a database session.

    Yields:
        Session: A SQLAlchemy database session.

    Examples:
        Usage within a FastAPI route:

        ```python
        from app.database import get_db

        @app.get("/users/{user_id}")
        def get_user(user_id: int, db: Session = Depends(get_db)):
            user = db.query(User).filter(User.id == user_id).first()
            return user
        ```
    """
    db = session
    print('start DB')
    try:
        yield db
    finally:
        pass
        # print('CLOSE DB')
        # db.close()
        