# -*- coding: utf-8 -*-
from flask_appbuilder import Model
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship


class ServiceParameter(Model):
    """Custom parameters for a Service (Many-to-One → Service)."""

    __tablename__ = "service_parameter"

    id = Column(Integer, primary_key=True)
    service_id = Column(Integer, ForeignKey("service.id", ondelete="CASCADE"), nullable=False)

    key = Column(String(255), nullable=False)  # e.g. "max_requests"
    value = Column(Text, nullable=True)  # e.g. "1000"

    label = Column(String(255))  # Human-readable label
    description = Column(Text)  # Optional hint / tooltip
    is_required = Column(Boolean, default=False)
    order = Column(Integer, default=0)  # Display order

    # back-reference to parent
    service = relationship("Service", back_populates="parameters")

    def __repr__(self):
        return f"<ServiceParameter {self.key}={self.value} (service_id={self.service_id})>"
