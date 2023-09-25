import json

from sqladmin import ModelView


class BaseModelView(ModelView):
    page_size = 15
    can_export = False
    form_excluded_columns = ['created_at', 'updated_at']

    def can_be_deleted(self, obj=None) -> bool:
        return False

    def key_in_search_list(self, key):
        search_list = [field.key for field in self.column_searchable_list]
        return key in search_list

    def get_search_value_by_key(self, key, params):
        try:
            fields = json.loads(params)
            return fields.get(key, '')
        except:
            return ''
