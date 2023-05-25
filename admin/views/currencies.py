from admin.views.base import BaseModelView
from app.modules.models import Currency


class CurrencyView(BaseModelView, model=Currency):
    icon = 'fa-solid fa-dollar-sign'
    name_plural = 'Currencies'
    column_list = [Currency.id, Currency.code, Currency.official_name]
    column_details_list = [Currency.id, Currency.code, Currency.official_name, Currency.name, Currency.name_plural, Currency.min_dep_amount, Currency.symbol, Currency.divider, Currency.exchange_rate]
    column_searchable_list = [Currency.code, Currency.official_name]
    column_sortable_list = [Currency.id, Currency.code, Currency.name]
    form_columns = [Currency.id, Currency.code, Currency.official_name, Currency.name, Currency.name_plural, Currency.min_dep_amount,Currency.symbol, Currency.divider, Currency.exchange_rate]
    #form_excluded_columns = ['created_at', 'updated_at']
