from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session
from starlette import status

from app.modules.models import Paragraph
from app.modules.schemas import ParagraphBaseSchema
from app.services.db import DatabaseServices

from app.modules.database import get_db

router = APIRouter(
    responses={404: {"description": "Not found"}},
)


@router.get('/')
def get_paragraphs(db: Session = Depends(get_db), limit: int = 10, page: int = 1):
    skip = (page - 1) * limit
    instances_list = DatabaseServices().get_list(db, Paragraph, limit, skip)
    return {'status': 'success', 'results': len(instances_list), 'paragraphs': instances_list}


@router.post('/', status_code=status.HTTP_201_CREATED)
def create_paragraph(payload: ParagraphBaseSchema, db: Session = Depends(get_db)):
    instance = DatabaseServices().create(db, Paragraph, **payload.dict())
    return {"status": "success", "paragraph": instance}


@router.patch('/{paragraph_id}')
def update_paragraph(paragraph_id: int, payload: ParagraphBaseSchema, db: Session = Depends(get_db)):
    instance = DatabaseServices().update(db, Paragraph, paragraph_id, **payload.dict(exclude_unset=True))
    return {"status": "success", "paragraph": instance}


@router.get('/{paragraph_id}')
def get_paragraph(paragraph_id: int, db: Session = Depends(get_db)):
    instance = DatabaseServices().get_by_id(db, Paragraph, paragraph_id)
    return {"status": "success", "paragraph": instance}

