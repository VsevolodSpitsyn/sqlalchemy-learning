"""make posts.title index

Revision ID: f590de6db44e
Revises: c81123d31544
Create Date: 2025-02-08 18:37:30.678542

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "f590de6db44e"
down_revision: Union[str, None] = "c81123d31544"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index(
        op.f("ix_blog_posts_title"), "blog_posts", ["title"], unique=False
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_blog_posts_title"), table_name="blog_posts")
    # ### end Alembic commands ###
