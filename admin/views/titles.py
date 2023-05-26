import datetime

from admin.views.base import BaseModelView
from app.modules.models import Title

formatters = {
    Title.template: lambda m, a: f'{m.template[:150]}... [{len(m.template)}]' if len(m.template) > 150 else m.template,
    Title.country: lambda m, a: m.country.name[:20] if m.country else '-',
    Title.language: lambda m, a: m.language.name[:20] if m.language else '-',
}


class TitleView(BaseModelView, model=Title):
    icon = 'fa-solid fa-comment'
    column_list = [Title.id, Title.template, Title.gender, Title.language, Title.language_id, Title.country,
                   Title.country_id]
    column_searchable_list = [Title.template, Title.gender, Title.language, Title.country]
    column_sortable_list = [Title.id, Title.template, Title.gender, Title.language_id, Title.country_id]
    column_formatters = formatters
    column_formatters_detail = formatters
    hints = {'template': [
        '{offer_name}',
        '{offer_hero}',
        '{tv_show_name}',
        '{currency_symbol}',
        '{central_bank}',
        '{offer_hero_first_name}',
        '{offer_hero_second_name}',
        '{country_demonym_capitalized}',
        '{country_demonym_plural_capitalized}',
        '{demonym}',
        '{demonym_plural}',
        '{currency_official_name}',
        '{currency_name_capitalized}',
        '{currency_name}',
        '{currency_name_plural}',
        '{min_dep_amount}',
        '{money_value}',
    ]}
    def can_be_deleted(self, obj=None) -> bool:
        return obj.created_at + datetime.timedelta(hours=1) > datetime.datetime.utcnow()
