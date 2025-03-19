# -*- coding: utf-8 -*-
import json
from flask_appbuilder import Model
from flask_appbuilder.models.mixins import AuditMixin
from sqlalchemy import Column, Float, Integer, DateTime, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app import appbuilder, db
from datetime import datetime
from flask import jsonify
import logging

_logger = logging.getLogger(__name__)


class Subscribe(Model, AuditMixin):
    id = Column(Integer, primary_key=True)
    name = Column(String)
    start_date = Column(
        DateTime,
        default=lambda: datetime.now().replace(microsecond=0),
        nullable=False,
    )
    total_amount = Column(Float)
    price = Column(Float)
    duration_month = Column(Integer)
    service_plan_id = Column(Integer, ForeignKey("service_plan.id"))
    service_plan = relationship("ServicePlan")
    parameters_values = relationship("ParameterValue")

    @property
    def service_details(self):

        if self.service_plan and self.service_plan.service:
            service = self.service_plan.service

            service_json = {}
            for key, value in service.__dict__.items():

                if not key.startswith('_'):
                    service_json[key] = value

            return service_json
        else:
            _logger.warning(
                "Service or service_plan is None for MyService ID %d", self.id)
            return {}

    def __repr__(self):
        return str(self.id)
