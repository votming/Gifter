from admin.views.base import BaseModelView
from app.modules.models import Role


class RoleView(BaseModelView, model=Role):
    icon = 'fa-solid fa-hammer'
    column_list = [Role.id, Role.name]
    column_searchable_list = [Role.id, Role.name]
    column_sortable_list = [Role.id, Role.name]
    form_excluded_columns = ['created_at', 'updated_at']

    def is_visible(self, request) -> bool:
        return request.scope['session']['role'] == 'admin'

    def is_accessible(self, request) -> bool:
        return request.scope['session']['role'] == 'admin'
