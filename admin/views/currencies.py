from admin.views.base import BaseModelView
from app.modules.models import Currency


class CurrencyView(BaseModelView, model=Currency):
    icon = 'fa-solid fa-dollar-sign'
    name_plural = 'Currencies'
    column_list = [Currency.id, Currency.code, Currency.name, Currency.name_en]
    column_details_list = [Currency.id, Currency.name, Currency.code, Currency.name_en, Currency.symbol]
    column_searchable_list = [Currency.code, Currency.name_en]
    column_sortable_list = [Currency.id, Currency.code, Currency.name, Currency.name_en]
    form_columns = [Currency.id, Currency.code, Currency.name, Currency.name_en, Currency.symbol]
    #form_excluded_columns = ['created_at', 'updated_at']
