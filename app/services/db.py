from fastapi import HTTPException
from starlette import status


class DatabaseServices:
    """Class providing database-related services."""

    def __init__(self, db, model):
        """
        Initialize a DatabaseServices instance.

        Args:
            db: The database object used for querying.
            model: The model representing the database table.
        """
        self.db = db
        self.model = model

    def get_list(self, limit, skip):
        """
        Retrieve a list of instances from the database.

        Args:
            limit (int): Maximum number of instances to retrieve.
            skip (int): Number of instances to skip.

        Returns:
            list: List of instances retrieved from the database.
        """
        instances = self.db.query(self.model).filter().limit(limit).offset(skip).all()
        return instances

    def create(self, **kwargs):
        """
        Create a new instance in the database.

        Args:
            **kwargs: Additional keyword arguments representing instance attributes.

        Returns:
            The created instance if successful.
        """
        instance = self.model(**kwargs)
        self.db.add(instance)
        self.db.commit()
        self.db.refresh(instance)
        return instance

    def update(self, pk, **payload):
        """
        Update an instance in the database by primary key.

        Args:
            pk: The primary key value of the instance to update.
            **payload: Additional keyword arguments representing attribute updates.

        Returns:
            The updated instance if successful.

        Raises:
            HTTPException: If no instance is found with the provided primary key.
        """
        query = self.db.query(self.model).filter(self.model.id == pk)
        instance = query.first()

        if not instance:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'No {self.model.__name__} with this id: {pk} found')
        query.filter(self.model.id == pk).update(payload, synchronize_session=False)
        self.db.commit()
        self.db.refresh(instance)
        return instance

    def get_by_id(self, pk):
        """
        Retrieve an instance from the database by primary key.

        Args:
            pk: The primary key value of the instance to retrieve.

        Returns:
            The retrieved instance if found.

        Raises:
            HTTPException: If no instance is found with the provided primary key.
        """
        instance = self.db.query(self.model).filter(self.model.id == pk).first()
        if not instance:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"No {self.model.__name__} with this id: {pk} found")
        return instance
