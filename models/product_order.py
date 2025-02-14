from sqlalchemy import (
    ForeignKey,
    Column,
    Integer,
    UniqueConstraint
)
from sqlalchemy.orm import relationship

from . import Base
from .mixins import TimestampMixin
from .order import Order
from .product import Product




class ProductOrder(TimestampMixin,Base):
    __tablename__ = "blog_products_in_orders"
    product_id = Column(
        ForeignKey(Product.id),
        # primary_key=True
    )
    order_id = Column(
        ForeignKey(Order.id),
        # primary_key=True
    )
    products_count = Column(
        Integer,
        nullable=False,
        default=1,
        server_default="1"
    )

    unit_price = Column(
        Integer,
        nullable=False,
    )


    product = relationship("Product", back_populates="orders")
    order = relationship("Order", back_populates="products")

    __table_args__ = (
        UniqueConstraint("product_id", "order_id", name='udx_product_order'),
    )

    def __repr__(self):
        return f"product_order[{self.product_id}, {self.order_id}]"