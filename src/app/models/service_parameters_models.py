from flask_appbuilder import Model
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship

class ServiceParameters(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    service_id = Column(Integer, ForeignKey("service.id"))
    service = relationship("Service",cascade="all,delete",)



    def __repr__(self):
            return self.name