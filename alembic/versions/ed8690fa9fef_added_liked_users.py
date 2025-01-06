"""added liked users

Revision ID: ed8690fa9fef
Revises: 1d3c6f6401a1
Create Date: 2025-01-03 11:22:13.537943

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ed8690fa9fef'
down_revision: Union[str, None] = '1d3c6f6401a1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('liked_users', sa.ARRAY(sa.BigInteger()), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'liked_users')
    # ### end Alembic commands ###