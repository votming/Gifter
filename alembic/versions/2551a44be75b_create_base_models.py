"""create_base_models

Revision ID: 2551a44be75b
Revises: 
Create Date: 2023-05-09 14:34:30.671555

"""
import os
import logging

from alembic import op
import sqlalchemy as sa
from sqlalchemy import func

from app.modules.database import session
from app.modules.models import Country
from app.modules.models import Currency
from app.modules.models import Language
from app.modules.models import Paragraph
from app.modules.models import Role
from app.modules.models import Title
from app.modules.models import User

logger = logging.getLogger(__name__)

# revision identifiers, used by Alembic.
revision = '2551a44be75b'
down_revision = None
branch_labels = None
depends_on = None


def create_objects(objects, model):
    for data in objects:
        instance = model(**data)
        session.add(instance)
    session.commit()

def upgrade() -> None:
    logger.error('CREATE TABLES')
    op.create_table(
        'user_roles',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(120)),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), onupdate=func.now())
    )
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('login', sa.String(120)),
        sa.Column('password', sa.String(120)),
        sa.Column('role_id', sa.Integer, nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), onupdate=func.now()),
        sa.ForeignKeyConstraint(('role_id',), ['user_roles.id'], ),
    )
    op.create_table(
        'currencies',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('official_name', sa.String(120)),
        sa.Column('name', sa.String(120)),
        sa.Column('name_plural', sa.String(120)),
        sa.Column('code', sa.String(5)),
        sa.Column('symbol', sa.String(5)),
        sa.Column('min_dep_amount', sa.String(120)),
        sa.Column('exchange_rate', sa.Integer, default=1),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), onupdate=func.now())
    )
    op.create_table(
        'countries',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('code', sa.String(2), nullable=False),
        sa.Column('divider', sa.String(3), default=''),
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
    op.create_table(
        'localizations',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('language_id', sa.Integer, nullable=False),
        sa.Column('country_id', sa.Integer, nullable=False),
        sa.Column('variable', sa.String(100)),
        sa.Column('value', sa.String(200)),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), onupdate=func.now()),
        sa.ForeignKeyConstraint(('language_id',), ['languages.id'], ),
        sa.ForeignKeyConstraint(('country_id',), ['countries.id'], ),
    )
    logger.error('TABLES CREATED')
    session.commit()
    roles = [{'name': 'admin'}, {'name': 'user'}]
    create_objects(roles, Role)
    chars = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
    admin_pass = "".join(chars[c % len(chars)] for c in os.urandom(12))
    print(f'Admin pass: {admin_pass}')
    user_pass = "".join(chars[c % len(chars)] for c in os.urandom(12))
    print(f'User pass: {user_pass}')
    users = [
        {'login': 'admin', 'password': admin_pass, 'role_id': 1},
        {'login': 'kislolord', 'password': "".join(chars[c % len(chars)] for c in os.urandom(12)), 'role_id': 1},
        {'login': 'votming', 'password': "".join(chars[c % len(chars)] for c in os.urandom(12)), 'role_id': 1},
        {'login': 'test_user', 'password': user_pass, 'role_id': 2}
    ]
    create_objects(users, User)
    languages = [{"name": 'English', 'code': "en"}, {'name': 'Spanish', 'code': "es"}]
    languages = [
    {'name': 'English', 'code': 'en'},
    {'name': 'Spanish', 'code': 'es'},
    {'name': 'French', 'code': 'fr'},
    {'name': 'Italian', 'code': 'it'},
    {'name': 'Swedish', 'code': 'sv'},
    {'name': 'Norwegian', 'code': 'no'},
    {'name': 'Danish', 'code': 'da'},
    {'name': 'Finnish', 'code': 'fi'},
    {'name': 'Dutch', 'code': 'nl'},
    {'name': 'Japanese', 'code': 'ja'}]
    create_objects(languages, Language)
    currencies = [{'official_name': 'US Dollars', 'name': 'dollar', 'name_plural': 'dollars', 'code': 'usd', 'symbol': '$'}, {'official_name': 'Euro', 'name': 'euro', 'name_plural': 'euros', 'code': 'eur', 'symbol': '€'}, {'official_name': 'Pound sterling', 'name': 'pound sterling', 'name_plural': 'pounds sterling', 'code': 'gbp', 'symbol': '£'}]
    currencies = [{
        # 1
        'code': 'USD',
        'official_name': 'United States Dollar',
        'name': 'dollar',
        'name_plural': 'dollars',
        'min_dep_amount': '250',
        'symbol': '$'
    },
    {
        # 2
        'code': 'EUR',
        'official_name': 'Euro',
        'name': 'euro',
        'name_plural': 'euros',
        'min_dep_amount': '250',
        'symbol': '€'
    },
    {
        # 3
        'code': 'GBP',
        'official_name': 'British Pound Sterling',
        'name': 'pound',
        'name_plural': 'pounds',
        'min_dep_amount': '250',
        'symbol': '£'
    },
    {
        # 4
        'code': 'JPY',
        'official_name': 'Japanese Yen',
        'name': 'yen',
        'name_plural': 'yens',
        'min_dep_amount': '250',
        'symbol': '¥'
    },
    {
        # 5
        'code': 'SEK',
        'official_name': 'Swedish Krona',
        'name': 'krona',
        'name_plural': 'kronas',
        'min_dep_amount': '250',
        'symbol': 'kr'
    },
    {
        # 6
        'code': 'NOK',
        'official_name': 'Norwegian Krone',
        'name': 'krona',
        'name_plural': 'kronas',
        'min_dep_amount': '250',
        'symbol': 'kr'
    },
    {
        # 7
        'code': 'CLP',
        'official_name': 'Chilean Peso',
        'name': 'peso',
        'name_plural': 'peso',
        'min_dep_amount': '250',
        'symbol': '$'
    },
    {
        # 8
        'code': 'MXN',
        'official_name': 'Peso Mexicano',
        'name': 'peso',
        'name_plural': 'peso',
        'min_dep_amount': '250',
        'symbol': '$'
    }]
    create_objects(currencies, Currency)
    countries = [{'name': 'United States', 'code': 'US', 'currency_id': 1, 'bank_name': 'US Bank'}, {'name': 'United Kingdom', 'code': 'GB', 'currency_id': 3, 'bank_name': 'UK Bank'}, {'name': 'Estonia', 'code': 'EN', 'currency_id': 1, 'bank_name': 'Estonian  Bank'}]
    countries = [
        {'name': 'United States', 'code': 'US', 'currency_id': 1, 'bank_name': 'US Bank', 'demonym': 'american', 'demonym_plural': 'americans',},
        {'code': 'UK', 'name': 'United Kingdom', 'demonym': 'british', 'demonym_plural': 'british',  'currency_id': 3,
         'bank_name': 'Bank of England'},
        {'code': 'AU', 'name': 'Australia', 'demonym': 'australian', 'demonym_plural': 'australians',  'currency_id': 1,
         'bank_name': 'Commonwealth Bank'},
        {'code': 'CA', 'name': 'Canada', 'demonym': 'canadian', 'demonym_plural': 'canadians',  'currency_id': 1,
         'bank_name': 'Bank of Canada'},
        {'code': 'ES', 'name': 'Spain', 'demonym': 'spanish', 'demonym_plural': 'spanish',  'currency_id': 2,
         'bank_name': 'Banco de España'},
        {'code': 'FR', 'name': 'France', 'demonym': 'french', 'demonym_plural': 'french',  'currency_id': 2,
         'bank_name': 'Banque de France'},
        {'code': 'IT', 'name': 'Italy', 'demonym': 'italian', 'demonym_plural': 'italians',  'currency_id': 2,
         'bank_name': 'Banca d\'Italia'},
        {'code': 'SE', 'name': 'Sweden', 'demonym': 'swedish', 'demonym_plural': 'swedes',  'currency_id': 5,
         'bank_name': 'Sveriges Riksbank'},
        {'code': 'NO', 'name': 'Norway', 'demonym': 'norwegian', 'demonym_plural': 'norwegians',  'currency_id': 6,
         'bank_name': 'Norges Bank'},
        {'code': 'DK', 'name': 'Denmark', 'demonym': 'danish', 'demonym_plural': 'danish',  'currency_id': 2,
         'bank_name': 'Danmarks Nationalbank'},
        {'code': 'FI', 'name': 'Finland', 'demonym': 'finnish', 'demonym_plural': 'finns',  'currency_id': 2,
         'bank_name': 'Bank of Finland'},
        {'code': 'NL', 'name': 'Netherlands', 'demonym': 'dutch', 'demonym_plural': 'dutch',  'currency_id': 2,
         'bank_name': 'De Nederlandsche Bank'},
        {'code': 'JP', 'name': 'Japan', 'demonym': 'japanese', 'demonym_plural': 'japanese',  'currency_id': 4,
         'bank_name': 'Bank of Japan'},
        {'code': 'CL', 'name': 'Chile', 'demonym': 'chilean', 'demonym_plural': 'chileans',  'currency_id': 7,
         'bank_name': 'Central Bank of Chile'},
        {'code': 'MX', 'name': 'Mexico', 'demonym': 'mexican', 'demonym_plural': 'mexicans',  'currency_id': 8,
         'bank_name': 'Bank of Mexico'}
    ]
    create_objects(countries, Country)
    titles = [
        {'gender': None, 'language_id': 1, 'country_id': None, 'template': "{offer_hero}’s latest investment has experts in awe and big banks terrified"},
        {'gender': None, 'language_id': 1, 'country_id': None, 'template': "Special report: {offer_hero}’s Latest Investment Has Experts in Awe And Big Banks Terrified"},
        {'gender': None, 'language_id': 1, 'country_id': None, 'template': "{offer_hero}'s investments impress experts and scare the minds of big banks"},
        {'gender': None, 'language_id': 1, 'country_id': None, 'template': "{offer_hero} invests $12 million in new trading platform – releases to public, making ordinary people wealthy"},
        {'gender': None, 'language_id': 1, 'country_id': None, 'template': "{offer_hero} reveals 'the rich society' secret: technology allowing everyone to earn millions"},
        {'gender': None, 'language_id': 1, 'country_id': None, 'template': "{offer_hero} shocked everyone in the studio by revealing how he is making an extra £128K every month"},
        {'gender': None, 'language_id': 1, 'country_id': 2, 'template': "{offer_hero} shocked everyone in the studio by revealing how he is making an extra $128K every month"},
        {'gender': None, 'language_id': 1, 'country_id': None, 'template': "{offer_hero}, Banks #1 wanted person, shared secret information on how to make a fortune"},
        {'gender': None, 'language_id': 1, 'country_id': None, 'template': "{offer_hero} accidentally revealed this top secret about a loophole that will make any {country_demonym_capitalized} rich"},
        {'gender': None, 'language_id': 1, 'country_id': None, 'template': "The gift of billionaire philanthropist {offer_hero} has secured the future of common people"},
        {'gender': 'male', 'language_id': 1, 'country_id': 2, 'template': "Bank of England sues {offer_hero} for what he said on live TV"},
        {'gender': 'female', 'language_id': 1, 'country_id': 2, 'template': "Bank of England sues {offer_hero} for what she said on live TV"},
        {'gender': 'male', 'language_id': 1, 'country_id': 3, 'template': "{offer_name} steals a march on everyone by making even more money after his new fiance revealed this new method of making money"},
        {'gender': 'male', 'language_id': 1, 'country_id': 2, 'template': "{offer_name} is being sued by the Bank of England for comments he made on live broadcast"},
        {'gender': 'male', 'language_id': 1, 'country_id': 2, 'template': "{offer_hero} shocked everyone in the studio by revealing how he is making an extra {currency_symbol}128K every month"},
    ]
    create_objects(titles, Title)
    paragraphs = [
        {'template': """The scandal erupted during a live broadcast when {offer_hero} accidentally revealed his secret on the program. Many viewers paid attention to {offer_hero_first_name}'s "accidental" words and began to send messages to the airwaves. However, the program was interrupted by a call from the {central_bank}, who demanded that the program be stopped immediately. """, 'language_id': 1, 'country_id': 1},
        {'template': """"The shocking truth was revealed on air, and {offer_hero} regretted it. However, it was too late.
The scandal erupted when {offer_hero_first_name} accidentally revealed her secret during a live broadcast. {offer_hero_first_name}'s ""accidental"" words captured the attention of many viewers, who began sending messages. As a result, the program was interrupted by the {central_bank}, which demanded that the program be halted immediately.
We were able to persuade the director of ""{tv_show_name}"" to provide us with a copy of the recording of this program. Keep in mind that this article, like the broadcast, may soon be deleted. In light of this, we would recommend you check out the link provided to us by {offer_hero} herself, if you happen to read this article. """, 'language_id': 1, 'country_id': None},
    ]
    create_objects(paragraphs, Paragraph)


def downgrade() -> None:
    op.drop_table('paragraphs')
    op.drop_table('titles')
    op.drop_table('countries')
    op.drop_table('languages')
    op.drop_table('currencies')
