# -*- coding: utf-8 -*-

from flask_appbuilder import Model
from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

from app import db


class ServiceTag(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    color = Column(String(255))
    services = relationship("Service", secondary="service_tag_association", back_populates="tags")

    def __repr__(self):
        return self.name


service_tag_association = Table(
    "service_tag_association",
    db.Model.metadata,
    Column("service_id", Integer, ForeignKey("service.id")),
    Column("tag_id", Integer, ForeignKey("service_tag.id")),
)
