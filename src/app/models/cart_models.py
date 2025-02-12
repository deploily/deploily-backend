# -*- coding: utf-8 -*-
from flask_appbuilder import Model
from sqlalchemy import Column
from sqlalchemy import Enum
from flask_appbuilder.security.sqla.models import User 
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import Float
from sqlalchemy.orm import relationship

class Cart(Model):
    id = Column(Integer, primary_key=True)
    status = Column(Enum("draft", "confirm", name="status"))  
    total_amount = Column(Float)
    user_id = Column(Integer, ForeignKey("ab_user.id"), nullable=False)  
    user = relationship("User")  
    def __repr__(self):
            return self.status