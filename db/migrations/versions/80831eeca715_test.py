"""test

Revision ID: 80831eeca715
Revises: 901eee9255e1
Create Date: 2023-05-03 14:19:37.130267

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '80831eeca715'
down_revision = '901eee9255e1'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'couriers', ['id'])
    op.add_column('stats_search', sa.Column('id', sa.Integer(), nullable=True))
    op.drop_constraint('stats_search_stat_id_key', 'stats_search', type_='unique')
    op.create_unique_constraint(None, 'stats_search', ['id'])
    op.drop_column('stats_search', 'stat_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('stats_search', sa.Column('stat_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'stats_search', type_='unique')
    op.create_unique_constraint('stats_search_stat_id_key', 'stats_search', ['stat_id'])
    op.drop_column('stats_search', 'id')
    op.drop_constraint(None, 'couriers', type_='unique')
    # ### end Alembic commands ###