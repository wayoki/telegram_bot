"""added liked users

Revision ID: 1d3c6f6401a1
Revises: 68de5f64d1e0
Create Date: 2025-01-03 11:11:18.015430

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1d3c6f6401a1'
down_revision: Union[str, None] = '68de5f64d1e0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
