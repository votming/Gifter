import datetime
from typing import (
    Optional,
)
from sqlalchemy.orm import (
    joinedload,
)
from sqlalchemy.sql.expression import Select
from sqlalchemy import Column, String, asc, cast, desc, func, inspect, or_
from admin.views.base import BaseModelView
from app.modules.models import Country
from app.modules.models import Title, Language
from sqladmin.pagination import Pagination

formatters = {
    Title.template: lambda m, a: f'{m.template[:150]}... [{len(m.template)}]' if len(m.template) > 150 else m.template,
    Title.country: lambda m, a: m.country.name[:20] if m.country else '-',
    Title.language: lambda m, a: m.language.name[:20] if m.language else '-',
}


class TitleView(BaseModelView, model=Title):
    icon = 'fa-solid fa-comment'
    column_list = [Title.id, Title.template, Title.gender, Title.language, Title.language_id, Title.country,
                   Title.country_id]
    #column_searchable_list = [Title.template, Title.gender, Title.language, Title.country]
    #column_searchable_list = [Title.template, Title.gender, Language.name, Country.name]
    column_searchable_list = [Title.template, Title.gender, Language.name, Country.name]
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


    async def list(
        self,
        page: int,
        page_size: int,
        search: Optional[str] = None,
        sort_by: Optional[str] = None,
        sort: str = "asc",
    ) -> Pagination:
        page_size = min(page_size or self.page_size, max(self.page_size_options))
        stmt = self.list_query.limit(page_size).offset((page - 1) * page_size)

        for relation in self._list_relation_attrs:
            stmt = stmt.outerjoin(relation).options(joinedload(relation))

        if sort_by:
            sort_fields = [(sort_by, sort == "desc")]
        else:
            sort_fields = self._get_default_sort()

        for sort_field, is_desc in sort_fields:
            if is_desc:
                stmt = stmt.order_by(desc(sort_field))
            else:
                stmt = stmt.order_by(asc(sort_field))

        if search:
            stmt = self.search_query(stmt=stmt, term=search)

        rows = await self._run_query(stmt)
        pagination = Pagination(
            rows=rows,
            page=page,
            page_size=page_size,
            count=len(rows),
        )

        return pagination

    def search_query(self, stmt: Select, term: str) -> Select:
        expressions = [
            cast(Title.template, String).ilike(f"%{term}%"),
            cast(Language.name, String).ilike(f"%{term}%"),
            cast(Country.name, String).ilike(f"%{term}%"),
            #cast(prop, String).ilike(f"%{term}%") for prop in self.column_searchable_list
        ]
        if term in {'male', 'female'}:
            expressions.append(or_(Title.gender == term, Title.gender == None))
        return stmt.filter(or_(*expressions))
