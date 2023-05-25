import json
import re
import traceback

from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy import func, or_
from sqlalchemy.orm import Session

from app.modules.models import Country
from app.modules.models import Currency
from app.modules.models import Language
from app.modules.models import Paragraph
from app.modules.models import Title

from app.modules.database import get_db
from app.utils.helpers import gather_template_variables

router = APIRouter(
    responses={404: {"description": "Not found"}},
)


@router.get('/get_data')
def get_title(
        offer_name: str | None = None,
        offer_hero_first_name: str | None = None,
        offer_hero_second_name: str | None = None,
        db: Session = Depends(get_db),
        language: str | None = None,
        gender: str | None = None,
        country: str | None = None,
        tv_show: str | None = None,
        currency: str | None = None,
        titles: str | None = None,
        featuring_image: str | None = None,
        paragraphs: str | None = None,
        macros: str | None = None
):
    if macros is not None:
        try:
            macros = {macro.split('=')[0]: macro.split('=')[1] for macro in macros.split(',')}
        except Exception:
            macros = dict()
    else:
        macros = dict()
    print(macros)
    try:
        response = {}
        #offer_name = f'{offer_hero_first_name} {offer_hero_second_name}'
        country_code = country
        if country_code is not None:
            country = Country.filter(code=country_code)
        currency_code = currency
        if currency_code is not None:
            print(currency_code)
            currency = Currency.filter(code=currency_code)
        language_code = language
        if language_code is not None:
            language = Language.filter(code=language_code)

        if titles is not None:
            title: Title = generate(db, Title, titles, country_code, language_code, gender)
            template = title.template
            if title is not None:
                template, money_values = parse_money_values(template)
                if currency is None and title.country is not None and title.country.currency is not None:
                    currency = title.country.currency
                demonym = title.country.demonym if title.country is not None else 'people'
                params = gather_template_variables(money_values=money_values, macros=macros, offer_name=offer_name, offer_hero_first_name=offer_hero_first_name, offer_hero_second_name=offer_hero_second_name, country_demonym_capitalized=demonym, currency=currency, languag=language, country=country)
                print(template)
                print(params)
                text = template.format(**params)
                response['title'] = text

        if paragraphs is not None:
            paragraph: Paragraph = generate(db, Paragraph, titles, country_code, language_code)
            template = paragraph.template
            if paragraph is not None:
                template, money_values = parse_money_values(template)
                bank_name = paragraph.country.bank_name if paragraph.country is not None else 'Bank'
                params = gather_template_variables(money_values=money_values, macros=macros, bank_name=bank_name, tv_show_name=tv_show, currency=currency, languag=language, country=country, offer_hero_first_name=offer_hero_first_name, offer_hero_second_name=offer_hero_second_name)
                text = template.format(**params)
                response['paragraph'] = text

        return response
    except Exception as ex:
        tb = traceback.format_exc()
        return {
            'error': str(ex),
            'traceback': tb
        }


def parse_money_values(template:str):
    money_placeholders = set(re.findall('{\d+}', template))
    money_values = dict()
    i = 1
    for value in money_placeholders:
        new_placeholder = f'money_value_{i}'
        template = template.replace(value, '{'+new_placeholder+'}')
        money_values[new_placeholder] = int(value.replace('{', '').replace('}', ''))
        i += 1
    return template, money_values

def generate(db, model, ids, country, language, gender=None):
    query = db.query(model)
    if ids != 'any':
        query = query.filter(model.id.in_(json.loads(ids)))
    if gender:
        query = query.filter(or_(model.gender == gender, model.gender == None))
    if country:
        query = query.join(Country, isouter=True).filter(or_(Country.code == country, model.country_id == None))
    if language:
        query = query.join(Language, isouter=True).filter(or_(Language.code == language, model.language_id == None))
    instance = query.order_by(func.random()).first()
    return instance
