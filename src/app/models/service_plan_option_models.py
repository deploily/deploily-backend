# -*- coding: utf-8 -*-
import json
from flask_appbuilder import Model
from flask_appbuilder.models.mixins import AuditMixin
from sqlalchemy import Column, Float, Integer, DateTime, String, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from app import appbuilder, db
from datetime import datetime
from flask import jsonify
import logging
from config import DB_LANGUAGES

_logger = logging.getLogger(__name__)


class ServicePlanOption(Model):
    id = Column(Integer, primary_key=True)
    service_plan_id = Column(Integer, ForeignKey(
        "service_plan.id"), nullable=False)
    service_plan = relationship("ServicePlan")
    icon = Column(String)
    html_content = Column(Text) 
    
    for lang in DB_LANGUAGES:
        if lang != 'en':
            locals()[f'html_content_{lang}'] = Column(Text, nullable=True)
    def __repr__(self):
        return f"{self.icon} {self.html_content}"
