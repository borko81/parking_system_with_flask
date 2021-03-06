"""Add document model, who save company data in aws cloud

Revision ID: cddb1424235b
Revises: b617ced24fdf
Create Date: 2021-12-15 17:28:00.606856

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cddb1424235b'
down_revision = 'b617ced24fdf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('documents',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('url', sa.String(), nullable=True),
    sa.Column('create_on', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('documents')
    # ### end Alembic commands ###
