import json
import random

from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy import func, or_
from sqlalchemy.orm import Session
from starlette import status

from modules.models import Country
from modules.models import Currency
from modules.models import Language
from modules.models import Paragraph
from modules.models import Title
from modules.schemas import TitleBaseSchema
from services.db import DatabaseServices

from modules.database import get_db

router = APIRouter(
    responses={404: {"description": "Not found"}},
)


@router.get('/get_data')
def get_title(
        offer_hero_first_name: str,
        offer_hero_second_name: str,
        db: Session = Depends(get_db),
        language: str = None,
        gender: str = None,
        country: str = None,
        tv_show: str = None,
        titles: str = None,
        featuring_image: str = None,
        paragraphs: str = None
):
    try:
        response = {}
        offer_name = f'{offer_hero_first_name} {offer_hero_second_name}'
        title_query = db.query(Title)
        if titles:
            title_query = title_query.filter(Title.id.in_(json.loads(titles)))
        if gender:
            title_query = title_query.filter(Title.gender == gender)
        if country:
            title_query = title_query.join(Country, isouter=True).filter(or_(Country.code == country, Title.country_id == None))
        if language:
            title_query = title_query.join(Language, isouter=True).filter(or_(Language.code == language, Title.language_id == None))
        title = title_query.order_by(func.random()).first()
        if title is None:
            return 'No title records were found with desired settings'
        if title.country is None or title.country.currency is None:
            currency = db.query(Currency).get(1)
        else:
            currency = title.country.currency
        demonym = title.country.demonym if title.country is not None else 'people'
        text = title.template.format(offer_name=offer_name, offer_hero=offer_name, country_demonym_capitalized=demonym, currency_symbol=currency.symbol)#{**title.__dict__, **title.country.__dict__, **title.language.__dict__})
        response['title'] = text
        if paragraphs:
            paragraph_query = db.query(Paragraph)
            if paragraphs:
                paragraph_query = paragraph_query.filter(Paragraph.id.in_(json.loads(paragraphs)))
            if country:
                paragraph_query = paragraph_query.join(Country, isouter=True).filter(or_(Country.code == country, Paragraph.country_id == None))
            if language:
                paragraph_query = paragraph_query.join(Language, isouter=True).filter(or_(Language.code == language, Paragraph.language_id==None))
            paragraph = paragraph_query.order_by(func.random()).first()
            if paragraph is not None:
                print(paragraph.country)
                bank_name = paragraph.country.bank_name if paragraph.country is not None else 'Bank'
                text = paragraph.template.format(offer_name=offer_name,offer_hero=offer_name, tv_show_name=tv_show, currency_symbol=currency.symbol, CENTRAL_BANK=bank_name, central_bank=bank_name, offer_hero_first_name=offer_hero_first_name,offer_hero_second_name=offer_hero_second_name)
                response['paragraph'] = text
        return response
    except Exception as ex:
        return str(ex)
