# -*- coding: utf-8 -*-
import logging

from flask_appbuilder import Model
from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

_logger = logging.getLogger(__name__)


class ServicePlanOption(Model):
    id = Column(Integer, primary_key=True)
    service_plan_id = Column(Integer, ForeignKey("service_plan.id"), nullable=False)
    service_plan = relationship("ServicePlan")
    icon = Column(String)
    html_content = Column(Text)

    def __repr__(self):
        return f"{self.icon} {self.html_content}"
