from sqlalchemy import (
    Table,
    ForeignKey,
    Column
)

from . import Base


posts_tags_association_table = Table(
    "posts_tags_association_table",
    Base.metadata,
    Column("post_id", ForeignKey("blog_posts.id"), primary_key=True),
    Column("tag_id", ForeignKey("blog_tags.id"), primary_key=True)

)