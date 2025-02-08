from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from . import Base
from .mixins import TimestampMixin


class Post(TimestampMixin, Base):
    title = Column(
        String(200), nullable=False, default="", server_default="", index=True
    )
    body = Column(Text, nullable=False, default="", server_default="")
    rating = Column(Integer, nullable=False, default=0, server_default="0")
    author_id = Column(Integer, ForeignKey("blog_authors.id"), nullable=False)
    author = relationship("Author", back_populates="posts")

    def __str__(self):
        return (
            f"{self.__class__.__name__}("
            f"title={self.title!r}, "
            f"rating={self.rating}, "
            f"author_id={self.author_id}, "
            f"body={self.body}"
        )
