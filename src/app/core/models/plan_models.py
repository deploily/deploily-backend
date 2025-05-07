# -*- coding: utf-8 -*-
from flask_appbuilder import Model
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


class Plan(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(String(255), nullable=False)
    service_plans = relationship("ServicePlan")

    def __repr__(self):
        return str(self.id)
