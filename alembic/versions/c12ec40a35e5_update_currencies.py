"""update currencies

Revision ID: c12ec40a35e5
Revises: 2551a44be75b
Create Date: 2023-05-25 21:37:48.268436

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c12ec40a35e5'
down_revision = '2551a44be75b'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('currencies', sa.Column('divider', sa.String(3), default=''))
    op.add_column('currencies', sa.Column('exchange_rate', sa.Float, default=1))
    pass


def downgrade() -> None:
    op.drop_column('currencies', 'exchange_rate')
    op.drop_column('currencies', 'divider')
