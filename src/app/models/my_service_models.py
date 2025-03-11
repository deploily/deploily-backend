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


class MyService(Model, AuditMixin):
    id = Column(Integer, primary_key=True)
    name = Column(String)
    start_date = Column(
        DateTime,
        default=lambda: datetime.now().replace(microsecond=0),
        nullable=False,
    )
    amount = Column(Float)
    duration_month = Column(Integer)
    is_active = Column(Boolean)
    service_plan_id = Column(Integer, ForeignKey("service_plan.id"))
    service_plan = relationship("ServicePlan")
    parameters_values = relationship("ParameterValue")

    @property
    def service_details(self):
        name = self.service_plan.service.name
        image_service = self.service_plan.service.image_service
        service = self.service_plan.service

        # service_json = {key: getattr(service, key)
        #                 for key in list(service.__dict__.keys())}
        service_json = {"name": name, "image_service": image_service}
        return service_json

        # _logger.info("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~é")
        # _logger.info(ddd)

        # return ddd
        # return jsonify(self.service_plan.service)

    def __repr__(self):
        return str(self.id)
