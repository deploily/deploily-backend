from flask_appbuilder import Model
from sqlalchemy import Column, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from flask_appbuilder.models.mixins import AuditMixin


class ContactUs(Model, AuditMixin):
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    message = Column(String(255), nullable=False)

    def __repr__(self):
        return self.name
