"""create_base_models

Revision ID: 2551a44be75b
Revises: 
Create Date: 2023-05-09 14:34:30.671555

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import func

from modules.database import session
from modules.models import Country
from modules.models import Currency
from modules.models import Language
from modules.models import Paragraph
from modules.models import Title

# revision identifiers, used by Alembic.
revision = '2551a44be75b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'currencies',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(120)),
        sa.Column('name_en', sa.String(120)),
        sa.Column('code', sa.String(5)),
        sa.Column('symbol', sa.String(5)),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), onupdate=func.now())
    )
    op.create_table(
        'countries',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('code', sa.String(2), nullable=False),
        sa.Column('demonym', sa.String(100), nullable=False),
        sa.Column('demonym_plural', sa.String(100), nullable=False),
        sa.Column('bank_name', sa.String(200), nullable=True),
        sa.Column('currency_id', sa.Integer, nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), onupdate=func.now()),
        sa.ForeignKeyConstraint(('currency_id',), ['currencies.id'], ),
    )
    op.create_table(
        'languages',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(120)),
        sa.Column('code', sa.String(3)),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), onupdate=func.now())
    )
    op.create_table(
        'titles',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('template', sa.Text),
        sa.Column('gender', sa.String(10), nullable=True),
        sa.Column('language_id', sa.Integer, nullable=False),
        sa.Column('country_id', sa.Integer, nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), onupdate=func.now()),
        sa.ForeignKeyConstraint(('language_id',), ['languages.id'], ),
        sa.ForeignKeyConstraint(('country_id',), ['countries.id'], ),
    )
    op.create_table(
        'paragraphs',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('template', sa.Text),
        sa.Column('number', sa.SmallInteger),
        sa.Column('language_id', sa.Integer, nullable=False),
        sa.Column('country_id', sa.Integer, nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), onupdate=func.now()),
        sa.ForeignKeyConstraint(('language_id',), ['languages.id'], ),
        sa.ForeignKeyConstraint(('country_id',), ['countries.id'], ),
    )
    languages = [{"name": 'English', 'code': "en"}, {'name':'Spanish', 'code': "es"}]
    for language in languages:
        instance = Language(**language)
        session.add(instance)
    session.commit()
    currencies = [{'name': 'US Dollars', 'name_en': 'US Dollars', 'code': 'usd', 'symbol': '$'}, {'name': 'Euro', 'name_en': 'Euro', 'code': 'eur', 'symbol': '€'}, {'name': 'Pound sterling', 'name_en': 'Pound sterling', 'code': 'gbp', 'symbol': '£'}]
    for currency in currencies:
        instance = Currency(**currency)
        session.add(instance)
    session.commit()
    countries = [{'name': 'United States', 'code': 'us', 'currency_id': 1, 'bank_name': 'US Bank'}, {'name': 'United Kingdom', 'code': 'gb','currency_id':3, 'bank_name': 'UK Bank'}, {'name': 'Estonia', 'code': 'en','currency_id':1, 'bank_name': 'Estonian  Bank'}]
    for country in countries:
        instance = Country(**country)
        session.add(instance)
    session.commit()
    titles = [
        {'template': "{offer_hero}’s latest investment has experts in awe and big banks terrified", 'gender': None, 'language_id': 1, 'country_id': None},
        {'template': "Special report: {offer_hero}’s Latest Investment Has Experts in Awe And Big Banks Terrified", 'gender': None, 'language_id': 1, 'country_id': None},
        {'template': "{offer_hero}'s investments impress experts and scare the minds of big banks", 'gender': None, 'language_id': 1, 'country_id': None},
        {'template': "{offer_hero} invests $12 million in new trading platform – releases to public, making ordinary people wealthy", 'gender': None, 'language_id': 1, 'country_id': None},
        {'template': "{offer_hero} reveals 'the rich society' secret: technology allowing everyone to earn millions", 'gender': None, 'language_id': 1, 'country_id': None},
        {'template': "{offer_hero} shocked everyone in the studio by revealing how he is making an extra £128K every month", 'gender': None, 'language_id': 1, 'country_id': None},
        {'template': "{offer_hero} shocked everyone in the studio by revealing how he is making an extra $128K every month", 'gender': None, 'language_id': 1, 'country_id': 2},
        {'template': "{offer_hero}, Banks #1 wanted person, shared secret information on how to make a fortune", 'gender': None, 'language_id': 1, 'country_id': None},
        {'template': "{offer_hero} accidentally revealed this top secret about a loophole that will make any {country_demonym_capitalized} rich", 'gender': None, 'language_id': 1, 'country_id': None},
        {'template': "The gift of billionaire philanthropist {offer_hero} has secured the future of common people", 'gender': None, 'language_id': 1, 'country_id': None},
        {'template': "Bank of England sues {offer_hero} for what he said on live TV", 'gender': 'male', 'language_id': 1, 'country_id': 2},
        {'template': "Bank of England sues {offer_hero} for what she said on live TV", 'gender': 'female', 'language_id': 1, 'country_id': 2},
        {'template': "{offer_name} steals a march on everyone by making even more money after his new fiance revealed this new method of making money", 'gender': 'male', 'language_id': 1, 'country_id': 3},
        {'template': "{offer_name} is being sued by the Bank of England for comments he made on live broadcast", 'gender': 'male', 'language_id': 1, 'country_id': 2},
        {'template': "{offer_hero} shocked everyone in the studio by revealing how he is making an extra {currency_symbol}128K every month", 'gender': 'male', 'language_id': 1, 'country_id': 2},
    ]
    for title in titles:
        instance = Title(**title)
        session.add(instance)
    session.commit()
    paragraphs = [
        {'template': """The scandal erupted during a live broadcast when {offer_hero} accidentally revealed his secret on the program. Many viewers paid attention to {offer_hero_first_name}'s "accidental" words and began to send messages to the airwaves. However, the program was interrupted by a call from the {CENTRAL_BANK}, who demanded that the program be stopped immediately. """, 'language_id': 1, 'country_id': 1},
        {'template': """"The shocking truth was revealed on air, and {offer_hero} regretted it. However, it was too late.
The scandal erupted when {offer_hero_first_name} accidentally revealed her secret during a live broadcast. {offer_hero_first_name}'s ""accidental"" words captured the attention of many viewers, who began sending messages. As a result, the program was interrupted by the {central_bank}, which demanded that the program be halted immediately.
We were able to persuade the director of ""{tv_show_name}"" to provide us with a copy of the recording of this program. Keep in mind that this article, like the broadcast, may soon be deleted. In light of this, we would recommend you check out the link provided to us by {offer_hero} herself, if you happen to read this article. """, 'language_id': 1, 'country_id': None},
    ]
    for paragraph in paragraphs:
        instance = Paragraph(**paragraph)
        session.add(instance)
    session.commit()


def downgrade() -> None:
    op.drop_table('titles')
    op.drop_table('languages')
    op.drop_table('currencies')
    op.drop_table('countries')
