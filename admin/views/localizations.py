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

    def is_visible(self, request) -> bool:
        return request.scope['session']['role'] == 'admin'

    def is_accessible(self, request) -> bool:
        return request.scope['session']['role'] == 'admin'
