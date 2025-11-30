"""add products table

Revision ID: e1ead0f3aba3
Revises: 9062f20a0ac7
Create Date: 2025-11-26 14:25:16.357235

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e1ead0f3aba3'
down_revision: Union[str, None] = '9062f20a0ac7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "products",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("tenant_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("category", sa.String(length=100), nullable=True),
        sa.Column("gender", sa.String(length=50), nullable=True),
        sa.Column("tags", sa.String(length=255), nullable=True),
        sa.Column("price", sa.Numeric(10, 2), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("image_url", sa.String(length=500), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.ForeignKeyConstraint(["tenant_id"], ["tenant.id"], ondelete="CASCADE"),
    )

    op.create_index("ix_products_tenant_id", "products", ["tenant_id"])
    op.create_index("ix_products_name", "products", ["name"])
    op.create_index("ix_products_category", "products", ["category"])
    op.create_index("ix_products_gender", "products", ["gender"])


def downgrade() -> None:
    op.drop_index("ix_products_gender", table_name="products")
    op.drop_index("ix_products_category", table_name="products")
    op.drop_index("ix_products_name", table_name="products")
    op.drop_index("ix_products_tenant_id", table_name="products")
    op.drop_table("products")
    # ### end Alembic commands ###
