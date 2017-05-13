"""empty message

Revision ID: 7065f3164ca3
Revises: 
Create Date: 2017-05-13 14:42:49.835428

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7065f3164ca3'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('clients',
    sa.Column('s_no', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('client_id', sa.String(), nullable=True),
    sa.Column('client_secret', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('s_no')
    )
    op.create_table('my_points',
    sa.Column('s_no', sa.Integer(), nullable=False),
    sa.Column('place', sa.String(), nullable=True),
    sa.Column('lat', sa.Float(), nullable=True),
    sa.Column('lon', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('s_no')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('my_points')
    op.drop_table('clients')
    # ### end Alembic commands ###
