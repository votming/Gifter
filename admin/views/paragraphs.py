import datetime

from admin.views.base import BaseModelView
from app.modules.models import Paragraph


class ParagraphView(BaseModelView, model=Paragraph):
    icon = 'fa-solid fa-newspaper'
    column_list = [Paragraph.id, Paragraph.template, Paragraph.language, Paragraph.country]
    column_searchable_list = [Paragraph.id, Paragraph.template, Paragraph.language,Paragraph.country]
    column_sortable_list = [Paragraph.id, Paragraph.template]
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
    column_formatters = {
        Paragraph.template: lambda m, a: f'{m.template[:150]}... [{len(m.template)}]' if len(m.template) > 150 else m.template,
        Paragraph.country: lambda m, a: m.country.name[:20] if m.country else '-',
        Paragraph.language: lambda m, a: m.language.name[:20] if m.language else '-',
    }

    def can_be_deleted(self, obj=None) -> bool:
        return obj.created_at + datetime.timedelta(hours=1) > datetime.datetime.utcnow()
