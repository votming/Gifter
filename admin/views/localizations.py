from admin.views.base import BaseModelView
from app.modules.models import Localization
from app.modules.models import User

#formatters = {Localization.role: lambda m, a: m.role.name}

class LocalizationView(BaseModelView, model=Localization):
    icon = 'fa-solid fa-globe'
    column_list = [Localization.id, Localization.variable, Localization.value, Localization.language, Localization.country]
    column_details_list = [Localization.id, Localization.language, Localization.country, Localization.variable, Localization.value]
    column_searchable_list = [Localization.variable]
    #column_sortable_list = [User.id, User.login, User.role_id]
    #form_columns = [User.id, User.login, User.password, User.role]
    #column_formatters_detail = formatters
    #column_formatters = formatters
    hints = {'variable': [
        'offer_name',
        'offer_hero',
        'tv_show_name',
        'currency_symbol',
        'central_bank',
        'offer_hero_first_name',
        'offer_hero_second_name',
        'country_demonym_capitalized',
        'country_demonym_plural_capitalized',
        'demonym',
        'demonym_plural',
        'currency_official_name',
        'currency_name_capitalized',
        'currency_name',
        'currency_name_plural',
        'min_dep_amount',
        'money_value',
    ]}
    def is_visible(self, request) -> bool:
        return request.scope['session']['role'] == 'admin'

    def is_accessible(self, request) -> bool:
        return request.scope['session']['role'] == 'admin'
