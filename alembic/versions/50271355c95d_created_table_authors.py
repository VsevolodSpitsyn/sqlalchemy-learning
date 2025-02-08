"""created table authors

Revision ID: 50271355c95d
Revises: 46906ce4f2d1
Create Date: 2025-02-08 18:22:55.012947

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "50271355c95d"
down_revision: Union[str, None] = "46906ce4f2d1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "blog_authors",
        sa.Column(
            "name", sa.String(length=20), server_default="", nullable=False
        ),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["blog_users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("blog_authors")
    # ### end Alembic commands ###
