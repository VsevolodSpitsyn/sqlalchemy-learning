"""create blog products in orders table

Revision ID: fde3d65e5cab
Revises: 5545a3e6e4d3
Create Date: 2025-02-14 20:54:26.030837

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "fde3d65e5cab"
down_revision: Union[str, None] = "5545a3e6e4d3"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "blog_products_in_orders",
        sa.Column("product_id", sa.Integer(), nullable=True),
        sa.Column("order_id", sa.Integer(), nullable=True),
        sa.Column(
            "products_count", sa.Integer(), server_default="1", nullable=False
        ),
        sa.Column("unit_price", sa.Integer(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["order_id"],
            ["blog_orders.id"],
        ),
        sa.ForeignKeyConstraint(
            ["product_id"],
            ["blog_products.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "product_id", "order_id", name="udx_product_order"
        ),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("blog_products_in_orders")
    # ### end Alembic commands ###
