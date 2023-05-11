from sqladmin import ModelView


class BaseModelView(ModelView):
    page_size = 15
    can_export = False
    form_excluded_columns = ['created_at', 'updated_at']

    def can_be_deleted(self, obj=None) -> bool:
        return False

