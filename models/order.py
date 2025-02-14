from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey
)
from sqlalchemy.orm import relationship

from . import Base
from .mixins import TimestampMixin

class Order(TimestampMixin, Base):

    address = Column(
        String,
        nullable=False
    )

    comment = Column(
        String,
        nullable=False,
        default="",
        server_default=""
    )

    user_id = Column(Integer,
                     ForeignKey("blog_users.id"),
                     nullable=False,
                     unique=True
                     )

    user = relationship("User", back_populates="orders")
    products = relationship("ProductOrder", back_populates="order")