from sqlalchemy import (
    Column,
    String
)
from sqlalchemy.orm import (
    relationship
)

from . import Base
from .posts_tags_association import posts_tags_association_table

class Tag(Base):
    name = Column(String(20), nullable=False, unique=True)

    posts = relationship("Post", back_populates= "tags", secondary=posts_tags_association_table)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"{self.__class__.__name__}(name={self.name!r})"
