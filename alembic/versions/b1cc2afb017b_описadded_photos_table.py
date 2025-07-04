"""Описadded photos table

Revision ID: b1cc2afb017b
Revises: 2817df33d945
Create Date: 2025-06-26 23:46:38.958240

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b1cc2afb017b'
down_revision: Union[str, None] = '2817df33d945'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_photos',
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.BigInteger(), nullable=False),
    sa.Column('file_url', sa.String(), nullable=False),
    sa.Column('file_name', sa.String(), nullable=False),
    sa.Column('media_type', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_photos')
    # ### end Alembic commands ###
