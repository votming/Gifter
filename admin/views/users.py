from admin.views.base import BaseModelView
from app.modules.models import User

formatters = {User.role: lambda m, a: m.role.name}

class UserView(BaseModelView, model=User):
    can_edit = False
    icon = 'fa-solid fa-user'
    column_list = [User.id, User.login, User.role, User.role_id]
    column_details_list = [User.id, User.login, User.role]
    column_searchable_list = [User.id, User.login, User.role]
    column_sortable_list = [User.id, User.login, User.role_id]
    form_columns = [User.id, User.login, User.password, User.role]
    column_formatters_detail = formatters
    column_formatters = formatters

    def is_visible(self, request) -> bool:
        return request.scope['session']['role'] == 'admin'

    def is_accessible(self, request) -> bool:
        return request.scope['session']['role'] == 'admin'
