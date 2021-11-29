"""Uncoment otc_id in park, becouse not view table otc

Revision ID: 6c3813f8df23
Revises: 95f15073e893
Create Date: 2021-11-29 14:46:04.189931

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6c3813f8df23'
down_revision = '95f15073e893'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('otc',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user_model.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('park', sa.Column('otc_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'park', 'otc', ['otc_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'park', type_='foreignkey')
    op.drop_column('park', 'otc_id')
    op.drop_table('otc')
    # ### end Alembic commands ###