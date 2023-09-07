from app.modules.database import session
from sqlalchemy import exc
import logging

logger = logging.getLogger(__name__)


class DBOperationsMixin:
    """Mixin class for common database operations."""

    @classmethod
    def get(cls, pk: int):
        """Retrieve a database instance by primary key.

        Args:
            pk (int): The primary key value.

        Returns:
            The instance of the class if found in the database.

        Raises:
            NoResultFound: If no instance is found with the provided primary key.
        """
        instance = session.query(cls).filter_by(id=pk).first()
        if instance:
            return instance
        raise exc.NoResultFound(f'{cls} not found')

    @classmethod
    def filter(cls, raise_exception=True, **filters):
        query = session.query(cls)
        query = query.filter_by(**filters)
        instance = query.first()
        if instance:
            return instance
        if raise_exception:
            raise exc.NoResultFound(f'Instance of the class {cls.__name__} not found')

    @classmethod
    def create(cls, **kwargs):
        """Create a new database instance.

        Args:
            **kwargs: Additional keyword arguments representing instance attributes.

        Returns:
            None
        """
        instance = cls(**kwargs)
        session.add(instance)
        session.commit()

    @classmethod
    def get_or_create(cls, **kwargs):
        """Retrieve a database instance by primary key, or create a new instance if not found.

        Args:
            **kwargs: Additional keyword arguments. Expected keyword: id (integer).

        Returns:
            The instance of the class if found in the database or a newly created instance.

        Raises:
            Exception: If `id` keyword argument is not provided.
        """
        if 'id' not in kwargs:
            raise Exception(f'Cannot search for a {cls} instance without an `id` field')
        instance = session.query(cls).filter_by(id=kwargs.get('id')).first()
        if instance:
            return instance
        instance = cls(**kwargs)
        session.add(instance)
        session.commit()
        return instance

    def update(self, **kwargs):
        """Update the attributes of a database instance.

        Args:
            **kwargs: Additional keyword arguments representing instance attribute updates.

        Returns:
            None
        """
        for key in kwargs.keys():
            setattr(self, key, kwargs.get(key))
            logger.info(f'[{self}] New `{key}` value is: {getattr(self, key)}')
        session.add(self)
        session.commit()

    def __repr__(self):
        """Return a string representation of the database instance.

        Returns:
            str: A string representation of the instance.
        """
        name = getattr(self, 'name_en', None) or getattr(self, 'name', None) or getattr(self, 'title', None) or \
               getattr(self, 'login', None) or getattr(self, 'id')
        return f'[{self.__class__.__name__}: {name}]'
