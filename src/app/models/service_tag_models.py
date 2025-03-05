from flask_appbuilder import Model
from sqlalchemy import Column, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class ServiceTag(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    color = Column(String(255))
    service_id = Column(Integer, ForeignKey("service.id"))
    service = relationship("Service")
    def __repr__(self):
        return self.name
