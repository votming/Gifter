from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session
from starlette import status

from app.modules.models import Country
from app.modules.schemas import CountryBaseSchema
from app.services.db import DatabaseServices

from app.modules.database import get_db

router = APIRouter(
    responses={404: {"description": "Not found"}},
)


@router.get('/')
def get_countries(db: Session = Depends(get_db), limit: int = 10, page: int = 1):
    skip = (page - 1) * limit
    instances_list = DatabaseServices().get_list(db, Country, limit, skip)
    return {'status': 'success', 'results': len(instances_list), 'countries': instances_list}


@router.post('/', status_code=status.HTTP_201_CREATED)
def create_country(payload: CountryBaseSchema, db: Session = Depends(get_db)):
    instance = DatabaseServices().create(db, Country, **payload.dict())
    return {"status": "success", "country": instance}


@router.patch('/{country_id}')
def update_country(country_id: int, payload: CountryBaseSchema, db: Session = Depends(get_db)):
    instance = DatabaseServices().update(db, Country, country_id, **payload.dict(exclude_unset=True))
    return {"status": "success", "country": instance}


@router.get('/{country_id}')
def get_country(country_id: int, db: Session = Depends(get_db)):
    instance = DatabaseServices().get_by_id(db, Country, country_id)
    return {"status": "success", "country": instance}
