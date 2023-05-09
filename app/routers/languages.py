from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session
from starlette import status

from app.modules.models import Language
from app.modules.schemas import LanguageBaseSchema
from app.services.db import DatabaseServices

from app.modules.database import get_db

router = APIRouter(
    responses={404: {"description": "Not found"}},
)


@router.get('/')
def get_language(db: Session = Depends(get_db), limit: int = 10, page: int = 1):
    skip = (page - 1) * limit
    instances_list = DatabaseServices(db, Language).get_list(limit, skip)
    return {'status': 'success', 'results': len(instances_list), 'languages': instances_list}


@router.post('/', status_code=status.HTTP_201_CREATED)
def create_language(payload: LanguageBaseSchema, db: Session = Depends(get_db)):
    instance = DatabaseServices(db, Language).create(**payload.dict())
    return {"status": "success", "language": instance}


@router.patch('/{Language_id}')
def update_language(language_id: int, payload: LanguageBaseSchema, db: Session = Depends(get_db)):
    instance = DatabaseServices(db, Language).update(language_id, **payload.dict(exclude_unset=True))
    return {"status": "success", "language": instance}


@router.get('/{Language_id}')
def get_language(language_id: int, db: Session = Depends(get_db)):
    instance = DatabaseServices(db, Language).get_by_id(language_id)
    return {"status": "success", "language": instance}
