from flask_appbuilder import Model
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Enum
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship


class Parameter(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    type = Column(Enum("token", "password", "port", name="type"))
    service_id = Column(Integer, ForeignKey("service.id"))
    service = relationship("Service", cascade="all,delete")
    parameters_values = relationship("ParameterValue")

    def __repr__(self):
        return self.name
