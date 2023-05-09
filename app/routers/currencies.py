from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session
from starlette import status

from app.modules.models import Currency
from app.modules.schemas import CurrencyBaseSchema
from app.services.db import DatabaseServices

from app.modules.database import get_db

router = APIRouter(
    responses={404: {"description": "Not found"}},
)


@router.get('/')
def get_currencies(db: Session = Depends(get_db), limit: int = 10, page: int = 1):
    skip = (page - 1) * limit
    instances_list = DatabaseServices(db, Currency).get_list(limit, skip)
    return {'status': 'success', 'results': len(instances_list), 'currencies': instances_list}


@router.post('/', status_code=status.HTTP_201_CREATED)
def create_currency(payload: CurrencyBaseSchema, db: Session = Depends(get_db)):
    instance = DatabaseServices(db, Currency).create(**payload.dict())
    return {"status": "success", "currency": instance}


@router.patch('/{currency_id}')
def update_currency(currency_id: int, payload: CurrencyBaseSchema, db: Session = Depends(get_db)):
    instance = DatabaseServices(db, Currency).update(currency_id, **payload.dict(exclude_unset=True))
    return {"status": "success", "currency": instance}


@router.get('/{currency_id}')
def get_currency(currency_id: int, db: Session = Depends(get_db)):
    instance = DatabaseServices(db, Currency).get_by_id(currency_id)
    return {"status": "success", "currency": instance}
