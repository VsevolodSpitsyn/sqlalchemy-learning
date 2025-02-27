"""Create users table

Revision ID: 8fe7f6d80b59
Revises:
Create Date: 2025-02-08 18:06:00.837376

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "8fe7f6d80b59"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "blog_users",
        sa.Column("username", sa.String(length=20), nullable=False),
        sa.Column(
            "is_staff", sa.Boolean(), server_default="FALSE", nullable=False
        ),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("username"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("blog_users")
    # ### end Alembic commands ###
