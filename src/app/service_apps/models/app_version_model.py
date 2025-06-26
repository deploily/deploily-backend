# -*- coding: utf-8 -*-

from flask_appbuilder import Model
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship


class Version(Model):
    __tablename__ = "version"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)  # e.g. "v1.0.0"
    description = Column(Text)

    app_services = relationship(
        "AppService", secondary="app_service_version", back_populates="app_versions"
    )

    def __repr__(self):
        return f"{self.name}"
