from sqlalchemy import (
    Column,
    String,
    Boolean,
)
from sqlalchemy.orm import relationship

from . import Base
from . import TimestampMixin


class User(TimestampMixin, Base):
    username = Column(String(20), unique=True, nullable=False)
    is_staff = Column(Boolean, nullable=False, default=False, server_default="FALSE")
    author = relationship("Author", back_populates="user", uselist=False)
    orders = relationship("Order", back_populates="user")

    def __str__(self):
        return (
            f"{self.__class__.__name__}("
            f"id={self.id}, "
            f"username={self.username!r}, "
            f"is_staff={self.is_staff}, "
            f"created_at={self.created_at})"
        )
