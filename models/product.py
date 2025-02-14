from sqlalchemy import (
    Column,
    String,
    Integer,
)
from sqlalchemy.orm import relationship
from . import Base
from .mixins import TimestampMixin


class Product(TimestampMixin,Base):
    name = Column(
        String(100),
        nullable=False)

    price = Column(
        Integer,
        nullable=False,
        default=0,
        server_default="0")

    orders = relationship("ProductOrder", back_populates="product")


    def __str__(self):
        return f"{self.__class__.__name__}(name={self.name!r}, price={self.price})"
