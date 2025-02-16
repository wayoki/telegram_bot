"""add viewed_users column

Revision ID: 68de5f64d1e0
Revises: 4bd1327e7333
Create Date: 2024-12-29 12:54:01.792619

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '68de5f64d1e0'
down_revision: Union[str, None] = '4bd1327e7333'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('viewed_users', sa.ARRAY(sa.BigInteger()), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'viewed_users')
    # ### end Alembic commands ###
