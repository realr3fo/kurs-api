"""empty message

Revision ID: e592942e0fce
Revises: 
Create Date: 2020-04-02 00:58:56.146436

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e592942e0fce'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('kurslists',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.Column('currency', sa.String(length=3), nullable=True),
    sa.Column('erate_jual', sa.String(length=20), nullable=True),
    sa.Column('erate_beli', sa.String(length=20), nullable=True),
    sa.Column('tt_counter_jual', sa.String(length=20), nullable=True),
    sa.Column('tt_counter_beli', sa.String(length=20), nullable=True),
    sa.Column('bank_notes_jual', sa.String(length=20), nullable=True),
    sa.Column('bank_notes_beli', sa.String(length=20), nullable=True),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.Column('date_modified', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('kurslists')
    # ### end Alembic commands ###