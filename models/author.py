from sqlalchemy import Column, String, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship

from . import Base


class Author(Base):
    name = Column(String(20), nullable=False, default="", server_default="")
    user_id = Column(Integer, ForeignKey("blog_users.id"), nullable=False, unique=True)
    user = relationship(
        "User",
        back_populates="author",
    )
    bio = Column(Text, nullable=False, default="", server_default="")
    posts = relationship("Post", back_populates="author")

    def __str__(self):
        return (
            f"{self.__class__.__name__}("
            f"id={self.id}, "
            f"author_name={self.name!r}, "
            f"user_id={self.user_id!r})"
        )
