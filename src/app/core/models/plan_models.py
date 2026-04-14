# -*- coding: utf-8 -*-
from flask_appbuilder import Model
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from config import DB_LANGUAGES


class Plan(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(String(255), nullable=False)
    for lang in DB_LANGUAGES:
        if lang != "en":
            locals()[f"description_{lang}"] = Column(String(255), nullable=True)
    service_plans = relationship("ServicePlan")

    def __repr__(self):
        return f"{self.name}"
