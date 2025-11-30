"""add products table

Revision ID: 3781fd4f3a5a
Revises: e607507d436e
Create Date: 2025-11-27 18:15:18.078147

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3781fd4f3a5a'
down_revision: Union[str, None] = 'e607507d436e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
