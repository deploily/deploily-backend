

from app.models.cart_line_models import CartLine
from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer


class TestInherit(CartLine):
    name = Column(Integer)
    # TODO add field
    pass
