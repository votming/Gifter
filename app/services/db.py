from fastapi import HTTPException
from starlette import status

#from modules.models import Chat, Message, User
#from telegram import Message as TelegramMessage


class DatabaseServices:

    def get_list(self, db, model, limit, skip):
        instances = db.query(model).filter().limit(limit).offset(skip).all()
        return instances

    def create(self, db, model, **kwargs):
        try:
            instance = model(**kwargs)
            db.add(instance)
            db.commit()
            db.refresh(instance)
            return instance
        except Exception as ex:
            return str(ex)

    def update(self, db, model, pk, **payload):
        query = db.query(model).filter(model.id == pk)
        instance = query.first()

        if not instance:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'No {model.__name__} with this id: {pk} found')
        query.filter(model.id == pk).update(payload, synchronize_session=False)
        db.commit()
        db.refresh(instance)
        return instance

    def get_by_id(self, db, model, pk):
        instance = db.query(model).filter(model.id == pk).first()
        if not instance:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"No {model.__name__} with this id: {pk} found")
        return instance
