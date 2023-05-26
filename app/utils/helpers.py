from app.modules.database import get_db
from app.modules.models import Country
from app.modules.models import Currency
from app.modules.models import Language
from app.modules.models import Localization


def gather_template_variables(money_values: dict, macros: dict, language: Language = None, country: Country = None, currency: Currency = None, **kwargs):
    first_name = kwargs.get('offer_hero_first_name', None)
    second_name = kwargs.get('offer_hero_second_name', None)
    offer_name = kwargs.get('offer_name', None)
    if offer_name is None and first_name is not None and second_name is not None:
        kwargs['offer_name'] = f'{first_name} {second_name}'
        kwargs['offer_hero'] = f'{first_name} {second_name}'
    demonym = kwargs.get('demonym', None) or (country.demonym if country else None)
    demonym_plural = kwargs.get('demonym_plural', None) or (country.demonym_plural if country else None)
    params = {
        'offer_name': kwargs.get('offer_name', None),
        'offer_hero': kwargs.get('offer_hero', None),
        'tv_show_name': kwargs.get('tv_show_name', None),
        'currency_symbol': currency.symbol if currency is not None else None,
        'central_bank': kwargs.get('bank_name', None) or (country.bank_name if country is not None else None),
        'offer_hero_first_name': kwargs.get('offer_hero_first_name', None),
        'offer_hero_second_name': kwargs.get('offer_hero_second_name', None),
        'country_demonym_capitalized': demonym.capitalize() if demonym else None,
        'country_demonym_plural_capitalized': demonym_plural.capitalize() if demonym_plural else None,
        'demonym': demonym,
        'demonym_plural': demonym_plural,
        'currency_official_name': kwargs.get('currency_official_name', None) or (currency.official_name if currency is not None else 'US Dollar'),
        'currency_name_capitalized': (kwargs.get('currency_name', None) or (currency.name if currency is not None else 'dollar')).capitalize(),
        'currency_name': kwargs.get('currency_name', None) or (currency.name if currency is not None else 'dollar'),
        'currency_name_plural': kwargs.get('currency_name_plural', None) or (currency.name_plural if currency is not None else 'dollars'),
        'min_dep_amount': kwargs.get('min_dep_amount', None) or (currency.min_dep_amount if currency is not None else '0 usd'),
        'money_value': kwargs.get('money_value', 1000000)
    }
    for key in money_values:
        if currency is not None:
            value = round(money_values[key] * (currency.exchange_rate or 1))
            money_values[key] = convert_money_value(value, (country.divider or '') if country is not None else '')
            # value = round(money_values[key] * (currency.exchange_rate or 1))
            # if value > 100:
            #     rounded = int(str(value)[:2])
            #     value = int(str(rounded) + '0' * (len(str(value)) - 2))
            # money_values[key] = f'{value:,}'.replace(',', currency.divider or '')
    localizations = dict()
    if language and country:
        localizations = {obj.variable: obj.value for obj in next(get_db()).query(Localization).filter(Localization.language_id == language.id, Localization.country_id == country.id).all()}
        print(f'LOCALIZTIONS: {localizations}')
    else:
        print(f'lang: {language}, country: {country}')
    output = params | localizations | macros
    print(f'CURRENCY IS {currency}')
    if currency is not None:
        output['money_value'] = f"{output['money_value']:,}".replace(',', (country.divider or '') if country is not None else  '')
    return params | localizations | money_values | macros  # {**params, **raw_data}


def convert_money_value(value, divider):
    if not isinstance(value, int):
        return value
    leading_part = int(str(value)[:3])
    rounding_part = float(f'0.{str(value)[3:]}')
    print(leading_part, rounding_part, round(rounding_part))
    if rounding_part < round(rounding_part):
        leading_part += 1
    value = int(str(leading_part) + '0' * (len(str(value)) - 3))
    return f'{value:,}'.replace(',', divider or '_')
