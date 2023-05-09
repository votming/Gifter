from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session
from starlette import status

from app.modules.models import Title
from app.modules.schemas import TitleBaseSchema
from app.services.db import DatabaseServices

from app.modules.database import get_db

router = APIRouter(
    responses={404: {"description": "Not found"}},
)


@router.get('/')
def get_titles(db: Session = Depends(get_db), limit: int = 10, page: int = 1):
    skip = (page - 1) * limit
    instances_list = DatabaseServices(db, Title).get_list(limit, skip)
    return {'status': 'success', 'results': len(instances_list), 'titles': instances_list}


@router.post('/', status_code=status.HTTP_201_CREATED)
def create_title(payload: TitleBaseSchema, db: Session = Depends(get_db)):
    instance = DatabaseServices(db, Title).create(**payload.dict())
    return {"status": "success", "title": instance}


@router.patch('/{title_id}')
def update_title(title_id: int, payload: TitleBaseSchema, db: Session = Depends(get_db)):
    instance = DatabaseServices(db, Title).update(title_id, **payload.dict(exclude_unset=True))
    return {"status": "success", "title": instance}


@router.get('/{title_id}')
def get_title(title_id: int, db: Session = Depends(get_db)):
    instance = DatabaseServices(db, Title).get_by_id(title_id)
    return {"status": "success", "title": instance}

