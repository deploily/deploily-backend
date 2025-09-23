from flask_appbuilder import Model
from sqlalchemy import Column, Integer, String, Text


class CustomParameter(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    # parameter_type = Column(Enum("string", "int", name="string"))
    value = Column(String(255), nullable=False)
