import datetime
from datetime import timezone

from admin.views.base import BaseModelView
from app.modules.models import Country

formatters = {Country.currency: lambda m, a: m.currency.name[:20]}


class CountryView(BaseModelView, model=Country):
    icon = 'fa-solid fa-earth-europe'
    name_plural = 'Countries'
    column_list = [Country.id, Country.name, Country.code, Country.bank_name, Country.currency, Country.currency_id]
    form_columns = [Country.currency, Country.name, Country.code, Country.demonym, Country.demonym_plural, Country.bank_name]
    column_details_list = [Country.id, Country.name, Country.code, Country.currency, Country.demonym, Country.demonym_plural, Country.bank_name]
    column_searchable_list = [Country.name, Country.code, Country.bank_name, Country.currency]
    column_sortable_list = [Country.id, Country.name, Country.code, Country.bank_name, Country.currency_id]
    column_formatters = formatters
    column_formatters_detail = formatters
