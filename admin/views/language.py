from admin.views.base import BaseModelView
from app.modules.models import Language


class LanguageView(BaseModelView, model=Language):
    icon = 'fa-solid fa-language'
    column_list = [Language.id, Language.name, Language.code]
    column_details_list = [Language.id, Language.name, Language.code]
    column_searchable_list = [Language.id, Language.name, Language.code]
    column_sortable_list = [Language.id, Language.name, Language.code]
    form_columns = [Language.id, Language.name, Language.code]
