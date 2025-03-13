

from app.models.service_models import Service
from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer


class TestInherit(Service):
    name = Column(Integer)
    # TODO add field
    pass
