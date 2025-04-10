"""empty message

Revision ID: 8736f1ce4fb6
Revises: 
Create Date: 2025-03-03 13:16:11.856761

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8736f1ce4fb6'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('ab_user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('phone', sa.String(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('ab_user', schema=None) as batch_op:
        batch_op.drop_column('phone')

    # ### end Alembic commands ###
