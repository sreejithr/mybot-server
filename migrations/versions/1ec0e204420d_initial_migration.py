"""Initial migration

Revision ID: 1ec0e204420d
Revises: 
Create Date: 2023-07-06 10:47:49.647187

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1ec0e204420d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('bot', schema=None) as batch_op:
        batch_op.add_column(sa.Column('history', sa.Text(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('bot', schema=None) as batch_op:
        batch_op.drop_column('history')

    # ### end Alembic commands ###
